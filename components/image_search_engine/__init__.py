import os
import numpy as np
import streamlit as st


@st.cache_data(ttl=3600)
def load_cache():
    """
    Load cache data

    :return images_name, descriptors: list of image names and descriptors corresponding to each image
    """

    DATASET_DIR = "./services/image_search_engine/val2017"
    images_name = os.listdir(os.path.join(DATASET_DIR, "images"))
    descriptors = []
    for image_name in images_name:
        image_name_no_ext = os.path.splitext(image_name)[0]
        descriptor = np.load(
            os.path.join(DATASET_DIR, "descriptors", f"{image_name_no_ext}.npy")
        )
        descriptors.append(descriptor)

    return images_name, descriptors
