import os
import numpy as np
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

    st.write(
        """
        - Nhận xét:
            - Đối với **SIFT**:
                - Ở các góc xoay nhỏ ($0\degree$ đến $20\degree$), SIFT có độ chính xác cao, gần bằng $1$.
                - Tuy nhiên, khi góc xoay tăng lên (khoảng từ $30\degree$ trở lên), 
                độ chính xác của **SIFT** giảm dần và duy trì ở mức khoảng $0.4$ đến $0.6$.
            - Đối với **ORB**:
                - **ORB** giữ được độ chính xác tốt hơn **SIFT** khi xoay ảnh, 
                với độ chính xác dao động quanh mức $0.5$ - $0.7$ ở các góc xoay từ $30\degree$ đến $350\degree$.
            - Đối với **SuperPoint**:
                - **SuperPoint** cho thấy độ chính xác cao nhất ở các góc nhỏ ($0\degree$ đến $10\degree$), nhưng giảm mạnh khi góc xoay lớn hơn.
                - Ở hầu hết các góc xoay từ $30\degree$ trở lên, độ chính xác của **SuperPoint** duy trì ở mức thấp, khoảng $0.2$ đến $0.4$. 
        """
    )

    st.write(
        "- Một số kết quả keypoint matching của $3$ thuật toán với góc xoay $10\degree$:"
    )
    cols = st.columns(3)
    cols[0].subheader("4.1. SIFT")
    cols[1].subheader("4.2. ORB")
    cols[2].subheader("4.3. SuperPoint")

    for type in [0, 1, 3, 4, 5, 6, 7]:
        cols = st.columns(3)

        sift_match_len = np.load(
            os.path.join(SERVICE_DIR, "results", f"sift_{type}_10.npy")
        )
        cols[0].image(
            os.path.join(SERVICE_DIR, "results", f"sift_{type}_10.png"),
            caption=f"{sift_match_len[0]} / {sift_match_len[1]} = {round(sift_match_len[0] / sift_match_len[1], 4)}% keypoints matched",
            use_column_width=True,
        )

        orb_match_len = np.load(
            os.path.join(SERVICE_DIR, "results", f"orb_{type}_10.npy")
        )
        cols[1].image(
            os.path.join(SERVICE_DIR, "results", f"orb_{type}_10.png"),
            caption=f"{orb_match_len[0]} / {orb_match_len[1]} = {round(orb_match_len[0] / orb_match_len[1], 4)}% keypoints matched",
            use_column_width=True,
        )

        superpoint_match_len = np.load(
            os.path.join(SERVICE_DIR, "results", f"superpoint_{type}_10.npy")
        )
        cols[2].image(
            os.path.join(SERVICE_DIR, "results", f"superpoint_{type}_10.png"),
            caption=f"{superpoint_match_len[0]} / {superpoint_match_len[1]} = {round(superpoint_match_len[0] / superpoint_match_len[1], 4)}% keypoints matched",
            use_column_width=True,
        )
