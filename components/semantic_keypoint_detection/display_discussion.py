import streamlit as st


@st.fragment()
def display_discussion():
    st.header("5. Thảo luận")
    st.write(
        """
        - **ORB** có ưu thế hơn **SIFT** cả **precision** và **recall** khi phát hiện keypoints trên $4$ loại hình checkboard, cube, polygon và star.
        - **SIFT** có ưu thế hơn **ORB** cả **precision** và **recall** khi phát hiện keypoints trên $2$ loại hình lines và stripes.
        - Ở loại hình **multiple polygons**, **ORB** có **precision** cao hơn **SIFT** nhưng **recall** lại thấp hơn.
        """
    )
