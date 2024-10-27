import os
import cv2
import numpy as np
import pandas as pd
import streamlit as st

from services.semantic_keypoint_detection.services import DATATYPES

pr_sift = np.load("./services/semantic_keypoint_detection/pr_sift.npy")
pr_orb = np.load("./services/semantic_keypoint_detection/pr_orb.npy")

pr_sift_fulls = []
pr_orb_fulls = []
for i in range(8):
    pr_sift_fulls.append(
        np.where(np.logical_and(pr_sift[i][:, 0] == 1, pr_sift[i][:, 1] == 1))[0]
    )
    pr_orb_fulls.append(
        np.where(np.logical_and(pr_orb[i][:, 0] == 1, pr_orb[i][:, 1] == 1))[0]
    )


@st.fragment()
def display_dataset():
    st.header("1. Số lượng ảnh phát hiện toàn bộ keypoint")
    cols = st.columns(2)

    data_df = pd.DataFrame(
        {
            "Loại": [
                DATATYPES[i].split("/")[-1].replace("draw_", "") for i in range(8)
            ],
            "SIFT": [len(pr_sift_fulls[i]) for i in range(8)],
            "ORB": [len(pr_orb_fulls[i]) for i in range(8)],
            "SIFT & ORB": [
                len(set(pr_sift_fulls[i]).intersection(pr_orb_fulls[i]))
                for i in range(8)
            ],
        }
    )

    st.write(
        "- Biểu đồ số lượng ảnh phát hiện toàn bộ keypoint bằng **SIFT** và **ORB**:"
    )
    st.bar_chart(
        data_df,
        x="Loại",
        y=["SIFT", "ORB", "SIFT & ORB"],
        x_label="",
        y_label="Số lượng ảnh",
        stack=False,
    )

    st.write("- Tổng số lượng ảnh phát hiện toàn bộ keypoint:")
    st.bar_chart(
        {
            "SIFT": sum(data_df["SIFT"]),
            "ORB": sum(data_df["ORB"]),
            "SIFT & ORB": sum(data_df["SIFT & ORB"]),
        },
        x_label="Số lượng ảnh",
        horizontal=True,
    )

    st.write("- Ảnh phát hiện toàn bộ keypoint bằng cả **SIFT** và **ORB**:")
    cols = st.columns(5)
    cnt = 0
    for i in range(8):
        for id in set(pr_sift_fulls[i]).intersection(pr_orb_fulls[i]):
            cols[cnt].image(
                os.path.join(DATATYPES[i], "images", f"{id}.png"), use_column_width=True
            )
            cnt += 1
