import os
import cv2
import numpy as np

DATASET_DIR = "./services/image_search_engine/val2017"
images_name = os.listdir(os.path.join(DATASET_DIR, "images"))

orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def search_image(img: cv2.typing.MatLike, top_k: int, mybar=None) -> list[str]:
    """
    Search for similar images to the input image

    :param img: input image
    :return: list of similar image paths
    """
    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, query_descriptors = orb.detectAndCompute(gray_scale, None)
    gray_scale_90 = cv2.rotate(gray_scale, cv2.ROTATE_90_CLOCKWISE)
    _, query_descriptors_90 = orb.detectAndCompute(gray_scale_90, None)
    gray_scale_180 = cv2.rotate(gray_scale, cv2.ROTATE_180)
    _, query_descriptors_180 = orb.detectAndCompute(gray_scale_180, None)
    gray_scale_270 = cv2.rotate(gray_scale, cv2.ROTATE_90_COUNTERCLOCKWISE)
    _, query_descriptors_270 = orb.detectAndCompute(gray_scale_270, None)

    results = []
    for image_name in images_name:
        image_name_no_ext = os.path.splitext(image_name)[0]
        descriptors = np.load(
            os.path.join(DATASET_DIR, "descriptors", f"{image_name_no_ext}.npy")
        )

        matches = bf.match(query_descriptors, descriptors)
        matches_90 = bf.match(query_descriptors_90, descriptors)
        matches_180 = bf.match(query_descriptors_180, descriptors)
        matches_270 = bf.match(query_descriptors_270, descriptors)

        results.append(
            (
                image_name,
                max(len(matches), len(matches_90), len(matches_180), len(matches_270)),
            )
        )

        if mybar is not None:
            mybar.progress(len(results) / len(images_name))

    results = sorted(results, key=lambda x: x[1], reverse=True)
    results = results[:top_k]
    return [os.path.join(DATASET_DIR, "images", result[0]) for result in results]
