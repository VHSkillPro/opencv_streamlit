import os
import cv2
import numpy as np
import pandas as pd
import streamlit as st

from services.semantic_keypoint_detection.services import (
    draw_points,
    get_average_pr_of_type_shape,
    sift,
    orb,
)

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


@st.fragment()
def display_datasets():
    st.header("1. Synthetic Shapes Datasets")
    st.write("- Tập dữ liệu gồm $8$ loại hình học cơ bản: ")

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
            - Mỗi loại hình học có $500$ ảnh mẫu.
            - Mỗi ảnh mẫu có kích thước $160$ x $120$ pixels.
        """
    )


@st.fragment()
def display_result_SIFT():
    st.header("2. Kết quả phát hiện keypoint bằng SIFT")
    st.subheader("2.1. Phát hiện keypoint trên ảnh mẫu")

    cols1 = st.columns(4)
    cols2 = st.columns(4)

    for i in range(4):
        image = cv2.imread(os.path.join(DATATYPES[i], "images", "0.png"))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints = sift.detect(gray, None)
        cv2.drawKeypoints(image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        cols1[i].image(
            image,
            use_column_width=True,
            caption=DATATYPES[i].split("/")[-1].replace("draw_", ""),
        )

    for i in range(4):
        image = cv2.imread(os.path.join(DATATYPES[i + 4], "images", "0.png"))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints = sift.detect(gray, None)
        cv2.drawKeypoints(image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        cols2[i].image(
            image,
            use_column_width=True,
            caption=DATATYPES[i + 4].split("/")[-1].replace("draw_", ""),
        )

    st.subheader("2.2. Đánh giá kết quả dựa trên độ đo Precision và Recall")
    cols = st.columns([3, 2], vertical_alignment="center", gap="large")
    cols[0].write(
        """
            - **Precision**: Tỷ lệ số keypoint phát hiện đúng trên tổng số keypoint phát hiện.
            - **Recall**: Tỷ lệ số keypoint phát hiện đúng trên tổng số keypoint thực sự.
            - Một keypoint được coi là phát hiện đúng nếu khoảng cách **Manhattan** giữa keypoint thực sự và keypoint phát hiện không lớn hơn $5$ pixels, với công thức $$d = |x_{true} - x_{pred}| + |y_{true} - y_{pred}|$$
            - **Precision** và **Recall** được tính trên tất cả các ảnh mẫu của tập dữ liệu và được tính trung bình.
            - Bảng kết quả **Precision** và **Recall** trung bình khi sử dụng SIFT trên từng loại hình:
        """
    )

    average_pr_SIFT = np.load(os.path.join(SERVICE_DIR, "average_pr_SIFT.npy"))
    df = pd.DataFrame(
        {
            "Loại hình": [
                DATATYPES[i].split("/")[-1].replace("draw_", "") for i in range(8)
            ],
            "Precision": average_pr_SIFT[:, 0],
            "Recall": average_pr_SIFT[:, 1],
        }
    )
    cols[0].dataframe(df, hide_index=True, use_container_width=True)

    st.write(
        f"""
        - **Precision** và **Recall** trung bình trên tất cả các loại hình:
            - **Precision** = ${np.mean(average_pr_SIFT[:, 0]):.4f}$
            - **Recall** = ${np.mean(average_pr_SIFT[:, 1]):.4f}$
    """
    )

    cols[1].image(
        os.path.join(SERVICE_DIR, "PR.png"),
        use_column_width=True,
        caption="Công thức của Precision và Recall",
    )


@st.fragment()
def display_result_ORB():
    st.header("3. Kết quả phát hiện keypoint bằng ORB")
    st.subheader("3.1. Phát hiện keypoint trên ảnh mẫu")

    cols1 = st.columns(4)
    cols2 = st.columns(4)

    for i in range(4):
        image = cv2.imread(os.path.join(DATATYPES[i], "images", "0.png"))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints = orb.detect(gray, None)
        cv2.drawKeypoints(image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        cols1[i].image(
            image,
            use_column_width=True,
            caption=DATATYPES[i].split("/")[-1].replace("draw_", ""),
        )

    for i in range(4):
        image = cv2.imread(os.path.join(DATATYPES[i + 4], "images", "0.png"))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        keypoints = orb.detect(gray, None)
        cv2.drawKeypoints(image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT)
        cols2[i].image(
            image,
            use_column_width=True,
            caption=DATATYPES[i + 4].split("/")[-1].replace("draw_", ""),
        )

    st.subheader("3.2. Đánh giá kết quả dựa trên độ đo Precision và Recall")
    st.write(
        """
            - Bảng kết quả **Precision** và **Recall** trung bình khi sử dụng ORB trên từng loại hình:
        """
    )

    average_pr_ORB = np.load(os.path.join(SERVICE_DIR, "average_pr_ORB.npy"))
    df = pd.DataFrame(
        {
            "Loại hình": [
                DATATYPES[i].split("/")[-1].replace("draw_", "") for i in range(8)
            ],
            "Precision": average_pr_ORB[:, 0],
            "Recall": average_pr_ORB[:, 1],
        }
    )
    st.dataframe(df, hide_index=True, use_container_width=True)

    st.write(
        f"""
        - **Precision** và **Recall** trung bình trên tất cả các loại hình:
            - **Precision** = ${np.mean(average_pr_ORB[:, 0]):.4f}$
            - **Recall** = ${np.mean(average_pr_ORB[:, 1]):.4f}$
    """
    )


@st.fragment()
def display_compare():
    st.header("4. So sánh kết quả giữa SIFT và ORB")

    average_pr_SIFT = np.load(os.path.join(SERVICE_DIR, "average_pr_SIFT.npy"))
    average_pr_ORB = np.load(os.path.join(SERVICE_DIR, "average_pr_ORB.npy"))

    df = pd.DataFrame(
        {
            "Loại hình": [
                DATATYPES[i].split("/")[-1].replace("draw_", "") for i in range(8)
            ],
            "Precision SIFT": average_pr_SIFT[:, 0],
            "Precision ORB": average_pr_ORB[:, 0],
            "Recall SIFT": average_pr_SIFT[:, 1],
            "Recall ORB": average_pr_ORB[:, 1],
        }
    )

    st.write(
        "- Bảng so sánh **Precision** và **Recall** trung bình giữa SIFT và ORB trên từng loại hình:"
    )
    st.dataframe(df, hide_index=True, use_container_width=True)
