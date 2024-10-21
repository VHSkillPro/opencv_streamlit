import os
import streamlit as st
from services.semantic_keypoint_detection.services import SERVICE_DIR


@st.fragment()
def display_evaluation():
    st.header("3. Đánh giá")
    st.write(
        """
        - Một keypoint được coi là phát hiện đúng nếu khoảng cách **Euclidean** giữa keypoint thực sự 
        và keypoint phát hiện không lớn hơn $5$ pixels, với công thức $$d = \sqrt{(x_{true} - x_{pred})^2 + (y_{true} - y_{pred})^2}$$
        - Hai độ đo **Precision** và **Recall** được sử dụng để đánh giá kết quả phát hiện keypoint của hai thuật toán **SIFT** và **ORB**
        với công thức:
        """
    )
    st.columns([1, 3, 1])[1].image(
        os.path.join(SERVICE_DIR, "PR.png"),
        use_column_width=True,
        caption="Precision và Recall",
    )
