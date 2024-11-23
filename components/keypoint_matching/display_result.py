import os, cv2
import numpy as np
import streamlit as st
from components.keypoint_matching import SERVICE_DIR
from services.keypoint_matching.service import (
    match_ORB,
    match_SIFT,
    match_SuperPoint,
    read_image,
    rotate_image,
    rotate_keypoints,
)
from services.keypoint_matching.superpoint import SuperPointFrontend
from services.semantic_keypoint_detection.services import DATATYPES

DATA_DIR = "services/semantic_keypoint_detection/synthetic_shapes_datasets"
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

    st.write(
        """
        - Nhận xét:
            - Đối với **SIFT**:
                - Ở các góc xoay nhỏ ($0\degree$ đến $30\degree$), **SIFT** có độ chính xác cao trên $0.6$, nhưng vẫn thấp nhất trong $3$ thuật toán.
                - Tuy nhiên, khi góc xoay tăng lên (khoảng từ $40\degree$ trở lên), độ chính xác của **SIFT** giảm dần dưới mức $0.3$.
            - Đối với **ORB**:
                - Ở các góc xoay nhỏ ($0\degree$ đến $30\degree$), **ORB** cho thấy độ chính xác cao hơn **SIFT**.
                - **ORB** giữ được độ chính xác tốt hơn **SIFT** và **SuperPoint** khi xoay ảnh với góc lớn (từ $40\degree$ đến $320\degree$),
                với độ chính xác dao động quanh mức $0.08$ - $0.23$ ở các góc xoay.
            - Đối với **SuperPoint**:
                - **SuperPoint** cho thấy độ chính xác cao nhất ở các góc nhỏ ($0\degree$ đến $30\degree$), nhưng giảm mạnh khi góc xoay lớn hơn.
                - Ở hầu hết các góc xoay từ $40\degree$ trở lên, độ chính xác của **SuperPoint** duy trì ở mức thấp, dưới $0.3$. 
        """
    )

    st.write(
        "- Một số kết quả keypoint matching của $3$ thuật toán với góc xoay tương ứng:"
    )
    cols = st.columns([1, 4])
    id_image = cols[0].number_input("Chọn ảnh", 0, 499, 0, 1)
    angle = cols[1].slider("Góc xoay", 0, 350, 10, 10)

    cols = st.columns(3)
    cols[0].subheader("4.1. SIFT")
    cols[1].subheader("4.2. ORB")
    cols[2].subheader("4.3. SuperPoint")

    for type in [0, 1, 3, 4, 5, 6, 7]:
        image, ground_truth = read_image(type, f"{id_image}")
        gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rotated_image = rotate_image(image, angle)
        rotated_gray_scale = cv2.cvtColor(rotated_image, cv2.COLOR_BGR2GRAY)

        h, w = rotated_gray_scale.shape
        rotated_keypoints, idx = rotate_keypoints((w, h), ground_truth, angle)
        original_keypoints = [ground_truth[i] for i in idx]

        sift_matches = match_SIFT(
            gray_scale, rotated_gray_scale, original_keypoints, rotated_keypoints
        )
        orb_matches = match_ORB(
            gray_scale, rotated_gray_scale, original_keypoints, rotated_keypoints
        )
        superpoint_matches = match_SuperPoint(
            gray_scale, rotated_gray_scale, original_keypoints, rotated_keypoints
        )

        sift_image_matches = cv2.drawMatches(
            image,
            original_keypoints,
            rotated_image,
            rotated_keypoints,
            sift_matches,
            None,
            matchColor=(0, 255, 0),
            singlePointColor=(255, 0, 0),
        )
        orb_image_matches = cv2.drawMatches(
            image,
            original_keypoints,
            rotated_image,
            rotated_keypoints,
            orb_matches,
            None,
            matchColor=(0, 255, 0),
            singlePointColor=(255, 0, 0),
        )
        superpoint_image_matches = cv2.drawMatches(
            image,
            original_keypoints,
            rotated_image,
            rotated_keypoints,
            superpoint_matches,
            None,
            matchColor=(0, 255, 0),
            singlePointColor=(255, 0, 0),
        )

        cols = st.columns(3)
        cols[0].image(
            sift_image_matches,
            caption=f"{len(sift_matches)} / {len(original_keypoints)} = {len(sift_matches) / len(original_keypoints):.2f}",
            use_column_width=True,
        )
        cols[1].image(
            orb_image_matches,
            caption=f"{len(orb_matches)} / {len(original_keypoints)} = {len(orb_matches) / len(original_keypoints):.2f}",
            use_column_width=True,
        )
        cols[2].image(
            superpoint_image_matches,
            caption=f"{len(superpoint_matches)} / {len(original_keypoints)} = {len(superpoint_matches) / len(original_keypoints):.2f}",
            use_column_width=True,
        )
