import os
import numpy as np
import pandas as pd
import streamlit as st
from services.semantic_keypoint_detection.services import SERVICE_DIR, DATATYPES

pr_sift: np.ndarray = np.load(os.path.join(SERVICE_DIR, "pr_sift.npy"))
pr_orb: np.ndarray = np.load(os.path.join(SERVICE_DIR, "pr_orb.npy"))


@st.fragment()
def display_results():
    st.header("4. Kết quả")

    precision_sift = pr_sift[:, :, 0]
    recall_sift = pr_sift[:, :, 1]
    precision_orb = pr_orb[:, :, 0]
    recall_orb = pr_orb[:, :, 1]

    average_precision_sift = precision_sift.mean(axis=1)
    average_recall_sift = recall_sift.mean(axis=1)
    average_precision_orb = precision_orb.mean(axis=1)
    average_recall_orb = recall_orb.mean(axis=1)

    cols = st.columns(2)
    with cols[0]:
        st.subheader("4.1 Đánh giá dựa trên độ đo Precision")
        precision_df = pd.DataFrame(
            {
                "shape_type": [
                    DATATYPES[i].split("/")[-1].replace("draw_", "")
                    for i in range(len(DATATYPES))
                ],
                "SIFT": average_precision_sift,
                "ORB": average_precision_orb,
            }
        )
        st.bar_chart(
            precision_df,
            x="shape_type",
            stack=False,
            y_label="",
            x_label="Precision",
            horizontal=True,
        )

    with cols[1]:
        st.subheader("4.2 Đánh giá dựa trên độ đo Recall")
        recall_df = pd.DataFrame(
            {
                "shape_type": [
                    DATATYPES[i].split("/")[-1].replace("draw_", "")
                    for i in range(len(DATATYPES))
                ],
                "SIFT": average_recall_sift,
                "ORB": average_recall_orb,
            }
        )
        st.bar_chart(
            recall_df,
            x="shape_type",
            stack=False,
            y_label="",
            x_label="Recall",
            horizontal=True,
        )
