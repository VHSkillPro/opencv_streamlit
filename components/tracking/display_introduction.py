import streamlit as st


@st.fragment()
def display_introduction():
    st.header("1. Giới thiệu")
    st.write(
        """
        - **Single Object Tracking (SOT)** là một lĩnh vực trong thị giác máy tính, tập trung vào việc theo dõi một đối tượng duy nhất trong một chuỗi video. 
        - Nhiệm vụ chính của **SOT** là xác định vị trí của đối tượng đã được chỉ định trong khung hình đầu tiên,
        sau đó liên tục theo dõi nó qua các khung hình tiếp theo, bất chấp những thay đổi về kích thước, góc nhìn, ánh sáng hoặc các vật cản khác.
        - Một số thuật toán **SOT** được hỗ trợ bởi **OpenCV** bao gồm **Boosting**, **MIL**, **KCF**, **TLD**, **MedianFlow**, **GOTURN**, **MOSSE** và **CSRT**.
        - Trong bài viết này, chúng ta sẽ tìm hiểu về thuật toán **KCF (Kernelized Correlation Filters)**.
        """
    )
