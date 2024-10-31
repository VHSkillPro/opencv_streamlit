import os
import numpy as np
import pandas as pd
import streamlit as st

from components.keypoint_matching import SERVICE_DIR

accuracy_rotations_sift = np.load(os.path.join(SERVICE_DIR, "results_sift.npy"))
accuracy_rotations_orb = np.load(os.path.join(SERVICE_DIR, "results_orb.npy"))
accuracy_rotations_superpoint = np.load(
    os.path.join(SERVICE_DIR, "results_superpoint.npy")
)


@st.fragment()
def display_result():
    st.header("4. Kết quả")
    st.bar_chart(
        {
            "SIFT": accuracy_rotations_sift,
            "ORB": accuracy_rotations_orb,
            "SuperPoint": accuracy_rotations_superpoint,
            "Góc quay": range(0, 360, 10),
        },
        x="Góc quay",
        y=["SIFT", "ORB", "SuperPoint"],
        y_label="Accuracy",
        x_label="Góc quay (độ)",
        stack=False,
        use_container_width=True,
    )
