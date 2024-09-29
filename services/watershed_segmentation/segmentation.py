import cv2
import numpy as np


def license_plate_watershed_segmentation(
    img: np.ndarray, kernel: np.ndarray, thres: float
) -> cv2.typing.MatLike:
    """
    Perform watershed segmentation on the license plate.

    Parameters
    ----------
        img: np.ndarray
            Input image to be segmented.
        kernel: np.ndarray
            Kernel used for morphological operations.
        thres: float
            Threshold value used for getting sure foreground area.
    """

    gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray_scale, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # noise removal
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    _, sure_fg = cv2.threshold(dist_transform, thres * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Marker labelling
    _, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    # Apply watershed
    markers = cv2.watershed(img, markers)

    return markers


def get_mask_license_plate(marks: cv2.typing.MatLike | np.ndarray) -> np.ndarray:
    """
    Get the mask of the license plate.

    Parameters
    ----------
        marks: cv2.typing.MatLike | np.ndarray
            Output of the watershed segmentation.
    """

    h, w = marks.shape
    mask = np.zeros((h, w), dtype=np.uint8)

    labels = np.unique(marks)
    for label in labels:
        if label == -1:
            continue

        min_w = np.min(np.where(marks == label)[1])
        max_w = np.max(np.where(marks == label)[1])
        min_h = np.min(np.where(marks == label)[0])
        max_h = np.max(np.where(marks == label)[0])

        ratio_w = (max_w - min_w) / w
        ratio_h = (max_h - min_h) / h

        check_ratio_w = 0 <= ratio_w and ratio_w <= 0.3
        check_ratio_h = 0.3 <= ratio_h and ratio_h <= 0.5

        if check_ratio_w and check_ratio_h:
            mask[marks == label] = 255

    return mask


def get_iou(ground_truth: np.ndarray, pred: np.ndarray) -> float:
    """
    Calculate the Intersection over Union (IoU) between the ground truth and the prediction.

    Parameters
    ----------
        ground_truth: np.ndarray
            Ground truth mask.
        pred: np.ndarray
            Predicted mask.
    """

    intersection = np.logical_and(ground_truth, pred)
    union = np.logical_or(ground_truth, pred)

    iou = np.sum(intersection) / np.sum(union)
    return iou


def get_dice(ground_truth: np.ndarray, pred: np.ndarray) -> float:
    """
    Calculate the Dice coefficient between the ground truth and the prediction.

    Parameters
    ----------
        ground_truth: np.ndarray
            Ground truth mask.
        pred: np.ndarray
            Predicted mask.
    """

    intersection = np.logical_and(ground_truth, pred)
    dice = 2 * np.sum(intersection) / (np.sum(ground_truth) + np.sum(pred))
    return dice
