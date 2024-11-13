import os
import cv2
import numpy as np
from components.image_search_engine import load_cache
from services.image_search_engine.superpoint import SuperPointFrontend

# fe = SuperPointFrontend(
#     "services/image_search_engine/superpoint_v1.pth",
#     nms_dist=4,
#     conf_thresh=0.015,
#     nn_thresh=0.7,
#     cuda=False,
# )
orb = cv2.ORB_create()
images_name, all_descriptors = load_cache()
DATASET_DIR = "./services/image_search_engine/val2017"

# FLANN_INDEX_KDTREE = 1
# index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
# search_params = dict(checks=50)
# flann = cv2.FlannBasedMatcher(index_params, search_params)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def search_image(
    img: cv2.typing.MatLike, top_k: int, cnt_image_query: int, mybar=None
) -> list[str]:
    """
    Search for similar images to the input image

    :param img: input image
    :return: list of similar image paths
    """
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_scales = [
        gray_scale,
        cv2.rotate(gray_scale, cv2.ROTATE_90_CLOCKWISE),
        cv2.rotate(gray_scale, cv2.ROTATE_180),
        cv2.rotate(gray_scale, cv2.ROTATE_90_COUNTERCLOCKWISE),
    ]
    query_descriptors = [orb.detectAndCompute(gray, None)[1] for gray in gray_scales]

    results = []
    for idx in range(min(cnt_image_query, len(images_name))):
        image_name = images_name[idx]
        train_descriptor = all_descriptors[idx]
        matches = [
            bf.match(query_descriptor, train_descriptor)
            for query_descriptor in query_descriptors
        ]

        # goods = []
        # for match in matches:
        #     if len(match) == 0 or len(match[0]) == 1:
        #         goods.append(0)
        #     else:
        #         cnt_good = 0
        #         for m, n in match:
        #             if m.distance < 0.7 * n.distance:
        #                 cnt_good += 1
        #         goods.append(cnt_good)

        similarity = []
        for i in range(len(matches)):
            similarity.append(len(matches[i]) / len(query_descriptors[i]))

        results.append(
            (
                image_name,
                np.max(similarity),
            )
        )

        if mybar is not None:
            mybar.progress(len(results) / min(len(images_name), cnt_image_query))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    results = results[:top_k]
    return [
        (os.path.join(DATASET_DIR, "images", result[0]), result[1])
        for result in results
    ]
