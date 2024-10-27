import os
import numpy as np
import pandas as pd
import streamlit as st

from components.keypoint_matching import SERVICE_DIR

accuracy_rotations_sift = np.load(
    os.path.join(SERVICE_DIR, "accuracy_rotations_sift.npy")
)
accuracy_rotations_orb = np.load(
    os.path.join(SERVICE_DIR, "accuracy_rotations_orb.npy")
)


@st.fragment()
def display_result():
    st.header("4. Kết quả")
    st.bar_chart(
        {
            "SIFT": accuracy_rotations_sift,
            "ORB": accuracy_rotations_orb,
            "Góc quay": range(0, 360, 10),
        },
        x="Góc quay",
        y=["SIFT", "ORB"],
        stack=False,
        use_container_width=True,
    )
