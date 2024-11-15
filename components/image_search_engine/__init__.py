import os
import cv2
import numpy as np
import streamlit as st


@st.cache_resource(ttl=3600)
def load_cache():
    """
    Load cache data

    :return images_name, descriptors: list of image names and descriptors corresponding to each image
    """

    DATASET_DIR = "./services/image_search_engine/val2017"
    images_name = os.listdir(os.path.join(DATASET_DIR, "images"))
    descriptors = []
    keypoints = []

    for image_name in images_name:
        image_name_no_ext = os.path.splitext(image_name)[0]
        descriptor = np.load(
            os.path.join(DATASET_DIR, "descriptors", f"{image_name_no_ext}.npy")
        )
        keypoint = np.load(
            os.path.join(DATASET_DIR, "keypoints", f"{image_name_no_ext}.npy")
        )
        keypoint = [
            cv2.KeyPoint(kp[0], kp[1], kp[2], kp[3], kp[4], int(kp[5]), int(kp[6]))
            for kp in keypoint
        ]

        descriptors.append(descriptor)
        keypoints.append(keypoint)

    return images_name, descriptors, keypoints
