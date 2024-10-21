import os
import cv2
import numpy as np
import streamlit as st


SERVICE_DIR = "./services/semantic_keypoint_detection"
DATASET_DIR = os.path.join(SERVICE_DIR, "synthetic_shapes_datasets")
DATATYPES = [
    os.path.join(DATASET_DIR, "draw_checkerboard"),
    os.path.join(DATASET_DIR, "draw_cube"),
    os.path.join(DATASET_DIR, "draw_ellipses"),
    os.path.join(DATASET_DIR, "draw_lines"),
    os.path.join(DATASET_DIR, "draw_multiple_polygons"),
    os.path.join(DATASET_DIR, "draw_polygon"),
    os.path.join(DATASET_DIR, "draw_star"),
    os.path.join(DATASET_DIR, "draw_stripes"),
]

sift = cv2.SIFT_create()
orb = cv2.ORB_create()


def draw_points(image: np.ndarray, points: np.ndarray, color=(0, 255, 0), thickness=2):
    for point in points:
        cv2.circle(image, (int(point[1]), int(point[0])), 1, color, thickness)
    return image


def get_pr(points: np.ndarray, pred_points: np.ndarray):
    tp, fp, fn = 0, 0, 0

    for point in points:
        if np.shape(pred_points)[0] > 0 and np.any(
            np.linalg.norm(pred_points - point, axis=1) <= 5
        ):
            tp += 1
        else:
            fn += 1

    for pred_point in pred_points:
        if np.shape(points)[0] == 0 or not np.any(
            np.linalg.norm(points - pred_point, axis=1) <= 5
        ):
            fp += 1

    if tp + fp == 0:
        return 0, 0
    if tp + fn == 0:
        return 0, 0
    return tp / (tp + fp), tp / (tp + fn)


def get_pr_of_type_shape(i: int, model):
    prs = []
    for j in range(500):
        points = np.load(os.path.join(DATATYPES[i], "points", f"{j}.npy"))
        image = cv2.imread(os.path.join(DATATYPES[i], "images", f"{j}.png"))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints = model.detect(gray, None)
        pred_points = np.array([[kp.pt[1], kp.pt[0]] for kp in keypoints])
        prs.append(get_pr(points, pred_points))
    return prs
