import os
import cv2
import numpy as np
from typing import Tuple, List
from services.keypoint_matching.superpoint import SuperPointFrontend
from services.semantic_keypoint_detection.services import DATATYPES

sift = cv2.SIFT_create()
orb = cv2.ORB_create(edgeThreshold=0, fastThreshold=0)
superpoint = SuperPointFrontend(
    weights_path="services/keypoint_matching/superpoint_v1.pth",
    nms_dist=4,
    conf_thresh=0.015,
    nn_thresh=0.7,
    cuda=False,
)


def read_image(type: int, name: str):
    """
    Reads an image and its ground truth keypoints from the specified dataset.

    :param type: The type of the dataset.
    :param name: The name of the image.

    :return (image, ground_truth): A tuple containing the image and the ground truth keypoints.
    """
    image = cv2.imread(os.path.join(DATATYPES[type], "images", f"{name}.png"))
    ground_truth = np.load(os.path.join(DATATYPES[type], "points", f"{name}.npy"))
    ground_truth = [cv2.KeyPoint(y, x, 1, 0, 0, 0) for x, y in ground_truth]
    return (image, ground_truth)


def rotate_image(image: cv2.typing.MatLike, angle: int) -> cv2.typing.MatLike:
    """
    Rotates an image by a given angle.

    :param image: The image to rotate.
    :param angle: The angle to rotate the image by.

    :return rotated_image: The rotated image.
    """
    h, w = image.shape[:2]
    matrix_rotation = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    rotated_image = cv2.warpAffine(image, matrix_rotation, (w, h))
    return rotated_image


def rotate_keypoints(
    size: Tuple[int, int], keypoints: List[cv2.KeyPoint], angle: int
) -> List[cv2.KeyPoint]:
    """
    Rotates the keypoints of an image.

    :param size: The size of the image (witdh, height).
    :param keypoints: The keypoints to rotate.
    :param angle: The angle to rotate the keypoints by.

    :return (result, idx): A tuple containing the rotated keypoints and their indices in the original list.
    """
    matrix_rotation = cv2.getRotationMatrix2D((size[0] / 2, size[1] / 2), angle, 1)
    kps = np.array([[kp.pt[0], kp.pt[1]] for kp in keypoints])
    kps = np.concatenate([kps, np.ones((len(kps), 1))], axis=1)
    rotated_kps = np.array(np.dot(matrix_rotation, kps.T)).T

    result, idx = [], []
    for i in range(len(rotated_kps)):
        kp = rotated_kps[i]
        if 0 <= kp[0] < size[0] and 0 <= kp[1] < size[1]:
            result.append(cv2.KeyPoint(kp[0], kp[1], 1, 0, 0, 0))
            idx.append(i)

    return (result, idx)


def match_SIFT(image1, image2, original_keypoints, rotated_keypoints):
    sift_original_descriptors = sift.compute(image1, original_keypoints)[1]
    sift_rotated_descriptors = sift.compute(image2, rotated_keypoints)[1]

    if len(sift_original_descriptors) == 1:
        return []

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(sift_rotated_descriptors, sift_original_descriptors, k=2)

    if len(sift_rotated_descriptors) == 1:
        return [matches[0]]

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance and m.trainIdx == m.queryIdx:
            good.append(m)
    return good


def match_ORB(image1, image2, original_keypoints, rotated_keypoints):
    orb_original_descriptors = orb.compute(image1, original_keypoints)[1]
    orb_rotated_descriptors = orb.compute(image2, rotated_keypoints)[1]

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(orb_rotated_descriptors, orb_original_descriptors)
    matches = [m for m in matches if m.queryIdx == m.trainIdx]
    return matches


def match_SuperPoint(image1, image2, original_keypoints, rotated_keypoints):
    image1 = image1.astype(np.float32) / 255.0
    image2 = image2.astype(np.float32) / 255.0

    superpoint_original_descriptors = superpoint.compute(image1, original_keypoints)[1]
    superpoint_rotated_descriptors = superpoint.compute(image2, rotated_keypoints)[1]

    if len(superpoint_original_descriptors) == 1:
        return []

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(
        superpoint_rotated_descriptors, superpoint_original_descriptors, k=2
    )

    if len(superpoint_rotated_descriptors) == 1:
        return [matches[0]]

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance and m.trainIdx == m.queryIdx:
            good.append(m)
    return good
