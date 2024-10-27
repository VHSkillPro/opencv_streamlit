import streamlit as st


@st.fragment()
def display_evaluation():
    st.header("3. Đánh giá")
    st.write(
        """
        - Đánh giá mức độ **Matching Keypoint** bằng **SIFT**, **ORB** và **SuperPoint** 
        trên tiêu chí **Rotation** với các góc quay $0\degree, 10\degree, 20\degree, ..., 360\degree$.
        - Đối với mỗi phương pháp, chỉ đánh giá trên tập ảnh đã phát hiện toàn bộ keypoint bằng phương pháp đó.
        - Độ đo được sử dụng là **accuracy**, được tính bằng tỉ lệ số keypoint matching đúng trên tổng số keypoint.
        """
    )
