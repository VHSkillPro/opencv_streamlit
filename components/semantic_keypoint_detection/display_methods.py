import os
import cv2
import numpy as np
import streamlit as st
from services.semantic_keypoint_detection.services import (
    DATATYPES,
    SERVICE_DIR,
    draw_points,
)

sift = cv2.SIFT_create()
orb = cv2.ORB_create()

pr_sift: np.ndarray = np.load(os.path.join(SERVICE_DIR, "pr_sift.npy"))
pr_orb: np.ndarray = np.load(os.path.join(SERVICE_DIR, "pr_orb.npy"))

precision_sift = pr_sift[:, :, 0]
recall_sift = pr_sift[:, :, 1]
precision_orb = pr_orb[:, :, 0]
recall_orb = pr_orb[:, :, 1]

id_image_of_type = [0 for _ in range(8)]
for type in range(8):
    if type == 2:
        continue

    idx = []
    if type in [0, 1, 4, 5, 6]:
        diff_precision = precision_orb[type] - precision_sift[type]
        diff_recall = recall_orb[type] - recall_sift[type]
        idx = np.where((diff_precision > 0) & (diff_recall > 0))[0]
    elif type == 7:
        diff_precision = precision_sift[type] - precision_orb[type]
        diff_recall = recall_sift[type] - recall_orb[type]
        idx = np.where((diff_precision > 0) & (diff_recall > 0))[0]
    else:
        diff_precision = precision_sift[type] - precision_orb[type]
        diff_recall = recall_orb[type] - recall_sift[type]
        idx = np.where((diff_precision > 0) & (diff_recall > 0))[0]

    precision = precision_orb[type][idx]
    recall = recall_orb[type][idx]
    pr = np.array([precision, recall]).T
    id_image_of_type[type] = idx[pr.min(axis=1).argmax()]


@st.fragment()
def display_methods():
    st.header("2. Phương pháp")

    cols_intro = st.columns(2)
    cols_algorithm = st.columns(2)
    cols_example = st.columns(2)

    with st.container():
        with cols_intro[0]:
            st.subheader("2.1. Thuật toán SIFT")
            st.markdown(
                """
                ##### 2.1.1. Giới thiệu về thuật toán SIFT
                - **SIFT** (Scale-Invariant Feature Transform) là một thuật toán được sử dụng để phát hiện và mô tả các keypoints trong hình ảnh.
                **SIFT** được giới thiệu bởi **David Lowe** vào năm **2004** trong bài báo 
                [*Distinctive Image Features from Scale-Invariant Keypoints*](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=cc58efc1f17e202a9c196f9df8afd4005d16042a).
                - **SIFT** có khả năng nhận diện đối tượng bất kể các biến đổi như xoay, thay đổi tỷ lệ, hoặc thay đổi ánh sáng.
                """
            )

        with cols_algorithm[0]:
            st.markdown("##### 2.1.2. Các bước chính của thuật toán SIFT:")
            st.image(
                os.path.join(SERVICE_DIR, "SIFT-process.png"), use_column_width=True
            )

        with cols_example[0]:
            st.markdown(
                "##### 2.1.3. Ví dụ trên Synthetic Shapes Dataset khi sử dụng SIFT:"
            )
            cols = [st.columns(2) for _ in range(4)]

            for i in range(8):
                idx = id_image_of_type[i]
                precision = precision_sift[i][idx]
                recall = recall_sift[i][idx]

                image = cv2.imread(os.path.join(DATATYPES[i], "images", f"{idx}.png"))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                keypoints = sift.detect(gray, None)

                ground_truth = np.load(
                    os.path.join(DATATYPES[i], "points", f"{idx}.npy")
                )
                image = draw_points(
                    image, [(kp.pt[1], kp.pt[0]) for kp in keypoints], (255, 0, 0), 2
                )
                image = draw_points(image, ground_truth, (0, 255, 0), 1, 5)

                r, c = i // 2, i % 2
                cols[r][c].image(
                    image,
                    use_column_width=True,
                    caption=f"Hình 2.1.3.{i + 1}: {DATATYPES[i].split("/")[-1].replace("draw_", "")} - Precision: {precision:.2f} - Recall: {recall:.2f}",
                )

    with st.container():
        with cols_intro[1]:
            st.subheader("2.2. Thuật toán ORB")
            st.markdown(
                """
                ##### 2.2.1. Giới thiệu về thuật toán ORB
                - **ORB** (Oriented FAST and Rotated BRIEF) là một thuật toán được sử dụng để phát hiện và mô tả các keypoints trong hình ảnh.
                **ORB** được giới thiệu bởi **Ethan Rublee**, **Vincent Rabaud**, **Kurt Konolige** và **Gary R. Bradski** vào năm **2011** trong bài báo 
                [*ORB: An efficient alternative to SIFT or SURF*](https://d1wqtxts1xzle7.cloudfront.net/90592905/145_s14_01-libre.pdf?1662172284=&response-content-disposition=inline%3B+filename%3DORB_An_efficient_alternative_to_SIFT_or.pdf&Expires=1729524210&Signature=dzhjTEuC-108NuiZwUIbVZStCXz5tryasM0l0sJpPx5kdMxzlIQ9ypiVK-Nrr7U4jRASqrmcG-7n0Q9nJhhEZpdOrtUd-Jw4zuBd53Z1tDUPa9BhZqImVlP3cQgAvMzsdoTsrV~yFTinoWzUKuuURdUn8jsWkqCgOzXur~sMPB4Svlihs-vGyIOL1b1hRbGLrNqwUM9KRXQAJuz2-kndG9S1zf-BReO262Qrjv7pmcgA6k4QdxajVDYqOnQDO89xUp2P0CjQwW0pwiOJ~RctdWw1fXQo2tmPPKvNsB-iXkOdKApkigZN27cAR2NH2NA39VOy~MkKHe1LefLCaSIeRw__&Key-Pair-Id=APKAJLOHF5GGSLRBV4ZA).
                - **ORB** là một phương pháp kết hợp giữa [**FAST**](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=e3d7f693bf2d3510a0557cda52c7547820fbef97) 
                (Feature from Accelerated Segment Test) và [**BRIEF**](https://infoscience.epfl.ch/server/api/core/bitstreams/730297d3-87f5-4580-877b-7064bc686198/content) (Binary Robust Independent Elementary Features).
                - Thuật toán **ORB** có ưu điểm là nhanh, hiệu quả và không bị ràng buộc bởi các vấn đề về bằng sáng chế như **SIFT**.
                """
            )

        with cols_algorithm[1]:
            st.markdown("##### 2.2.2. Các bước chính của thuật toán ORB:")
            st.image(
                os.path.join(SERVICE_DIR, "ORB-process.png"), use_column_width=True
            )

        with cols_example[1]:
            st.markdown(
                "##### 2.2.3. Ví dụ trên Synthetic Shapes Dataset khi sử dụng ORB:"
            )
            cols = [st.columns(2) for _ in range(4)]

            for i in range(8):
                idx = id_image_of_type[i]
                precision = precision_orb[i][idx]
                recall = recall_orb[i][idx]

                image = cv2.imread(os.path.join(DATATYPES[i], "images", f"{idx}.png"))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                keypoints = orb.detect(gray, None)

                ground_truth = np.load(
                    os.path.join(DATATYPES[i], "points", f"{idx}.npy")
                )
                image = draw_points(
                    image, [(kp.pt[1], kp.pt[0]) for kp in keypoints], (255, 0, 0), 2
                )
                image = draw_points(image, ground_truth, (0, 255, 0), 1, 5)

                r, c = i // 2, i % 2
                cols[r][c].image(
                    image,
                    use_column_width=True,
                    caption=f"Hình 2.2.3.{i + 1}: {DATATYPES[i].split("/")[-1].replace("draw_", "")} - Precision: {precision:.2f} - Recall: {recall:.2f}",
                )

        st.write(
            """
            - Các vòng tròn màu **:green[xanh lục]** là **keypoints** từ **ground truth** có bán kính là $5$ pixels.
            - Các hình tròn màu **:red[đỏ]** là **keypoints** được phát hiện bởi thuật toán **SIFT** và **ORB**.
            """
        )
