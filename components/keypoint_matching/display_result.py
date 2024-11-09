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
