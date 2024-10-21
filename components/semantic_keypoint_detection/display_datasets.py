import os
import cv2
import numpy as np
import streamlit as st
from services.semantic_keypoint_detection.services import draw_points, DATATYPES


@st.fragment()
def display_datasets():
    st.header("1. Synthetic Shapes Datasets")
    st.write(
        """
        - **Synthetic Shapes Datasets** là bộ dữ liệu được tổng hợp từ các hình học 2D 
        đơn giản thông qua kết hợp các hình cơ bản như hình vuông, hình tròn, hình elip, 
        hình sao, hình đa giác, hình đa giác nhiều cạnh, hình dải, hình ô vuông, hình đường thẳng. 
        Tập dữ liệu gồm $8$ loại hình học cơ bản: 
    """
    )

    cols1 = st.columns(4)
    cols2 = st.columns(4)

    for i in range(4):
        points = np.load(os.path.join(DATATYPES[i], "points", "0.npy"))
        image = cv2.imread(os.path.join(DATATYPES[i], "images", "0.png"))
        cols1[i].image(
            draw_points(image, points),
            use_column_width=True,
            caption=DATATYPES[i].split("/")[-1].replace("draw_", ""),
        )

    for i in range(4):
        points = np.load(os.path.join(DATATYPES[i + 4], "points", "0.npy"))
        image = cv2.imread(os.path.join(DATATYPES[i + 4], "images", "0.png"))
        cols2[i].image(
            draw_points(image, points),
            use_column_width=True,
            caption=DATATYPES[i + 4].split("/")[-1].replace("draw_", ""),
        )

    st.write(
        """
            - Mỗi loại hình học có $500$ ảnh mẫu, tổng cộng $4000$ ảnh mẫu.
            - Mỗi ảnh mẫu có kích thước $160$ x $120$ pixels.
        """
    )
