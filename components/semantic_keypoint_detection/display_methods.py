import os
import cv2
import streamlit as st
from services.semantic_keypoint_detection.services import DATATYPES, SERVICE_DIR

sift = cv2.SIFT_create()
orb = cv2.ORB_create()


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
            st.markdown("##### 2.1.3. Ví dụ trên Synthetic Shapes Datasets:")
            cols = [st.columns(2) for _ in range(4)]

            for i in range(8):
                image = cv2.imread(os.path.join(DATATYPES[i], "images", "0.png"))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                keypoints = sift.detect(gray, None)
                cv2.drawKeypoints(
                    image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT
                )
                r, c = i // 2, i % 2
                cols[r][c].image(
                    image,
                    use_column_width=True,
                    caption=DATATYPES[i].split("/")[-1].replace("draw_", ""),
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
                - **ORB** là một phương pháp kết hợp giữa **FAST** (Feature from Accelerated Segment Test) và **BRIEF** (Binary Robust Independent Elementary Features).
                - Thuật toán **ORB** có ưu điểm là nhanh, hiệu quả và không bị ràng buộc bởi các vấn đề về bằng sáng chế như **SIFT**.
                """
            )

        with cols_algorithm[1]:
            st.markdown("##### 2.2.2. Các bước chính của thuật toán ORB:")
            st.image(
                os.path.join(SERVICE_DIR, "ORB-process.png"), use_column_width=True
            )

        with cols_example[1]:
            st.markdown("##### 2.2.3. Ví dụ trên Synthetic Shapes Datasets:")
            cols = [st.columns(2) for _ in range(4)]

            for i in range(8):
                image = cv2.imread(os.path.join(DATATYPES[i], "images", "0.png"))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                keypoints = orb.detect(gray, None)
                cv2.drawKeypoints(
                    image, keypoints, image, flags=cv2.DRAW_MATCHES_FLAGS_DEFAULT
                )
                r, c = i // 2, i % 2
                cols[r][c].image(
                    image,
                    use_column_width=True,
                    caption=DATATYPES[i].split("/")[-1].replace("draw_", ""),
                )
