import os
import cv2
import numpy as np
from components.image_search_engine import load_cache
from services.image_search_engine.superpoint import SuperPointFrontend

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

images_name, all_descriptors, all_keypoints = load_cache()
DATASET_DIR = "./services/image_search_engine/val2017"


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

    # query_keypoints = []
    query_descriptors = []
    for i in range(len(gray_scales)):
        keypoints, descriptors = orb.detectAndCompute(gray_scales[i], None)
        # query_keypoints.append(keypoints)
        query_descriptors.append(descriptors)

    results = []
    for idx in range(min(cnt_image_query, len(images_name))):
        image_name = images_name[idx]
        train_descriptor = all_descriptors[idx]
        # train_keypoints = all_keypoints[idx]
        matches = [
            bf.match(query_descriptor, train_descriptor)
            for query_descriptor in query_descriptors
        ]

        similarity = []
        for i in range(len(matches)):
            similarity.append(len(matches[i]) / len(query_descriptors[i]))
            # if len(matches[i]) > 10:
            #     src_pts = np.float32(
            #         [query_keypoints[i][m.queryIdx].pt for m in matches[i]]
            #     ).reshape(-1, 1, 2)
            #     dst_pts = np.float32(
            #         [train_keypoints[m.trainIdx].pt for m in matches[i]]
            #     ).reshape(-1, 1, 2)

            #     M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            #     matchesMask = mask.ravel().tolist()
            #     similarity.append(np.sum(matchesMask) / len(query_descriptors[i]))
            # else:
            #     similarity.append(0)

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
