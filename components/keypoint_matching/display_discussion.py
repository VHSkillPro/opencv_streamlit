import streamlit as st


@st.fragment()
def display_discussion():
    st.header("5. Thảo luận")
    st.write(
        """
        - **ORB** và **SIFT** có độ chính xác cao hơn khi ảnh bị xoay mạnh, trong khi **SuperPoint** kém hiệu quả hơn trong điều kiện này.
        - **SuperPoint** chỉ hiệu quả khi ảnh không bị xoay mạnh (dưới $30\degree$).
        - **ORB** đạt hiệu quả cao khi xoay nhẹ và duy trì độ chính xác khá ổn định ở các góc xoay lớn, với độ chính xác vượt trội ở nhiều góc (đặc biệt là ở $0\degree$ và gần $180\degree$).
        - **SIFT** ổn định hơn **ORB**, đạt độ chính xác cao và ổn định ở nhiều góc xoay khác nhau, đặc biệt tốt ở các góc $180\degree$ và $270\degree$.
        """
    )
