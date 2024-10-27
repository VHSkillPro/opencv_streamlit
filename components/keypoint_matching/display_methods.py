import streamlit as st


@st.fragment()
def display_methods():
    st.header("2. Phương pháp")
    st.write(
        """
        - **SuperPoint** là một mô hình deep learning được huấn luyện để phát hiện các keypoints trên ảnh, 
        được đề xuất bởi **Daniel DeTone**, **Tomasz Malisiewicz**, **Andrew Rabinovich** vào năm 2018 
        trong bài báo [SuperPoint: Self-Supervised Interest Point Detection and Description](https://arxiv.org/abs/1712.07629).
        - Kiến trúc của mô hình **SuperPoint** gồm 3 phần chính: **Shared Encoder**, **Interest Point Detector** và **Descriptor Decoder**.
        """
    )
    st.columns([1, 4, 1])[1].image(
        "https://www.researchgate.net/publication/381372557/figure/fig1/AS:11431281251582233@1718249424443/The-model-architecture-of-the-SuperPoint3.ppm",
        caption="Kiến trúc của mô hình SuperPoint",
        use_column_width=True,
    )
    st.write(
        """
        - Đầu vào của mô hình là ảnh grayscale có kích thước $W$ x $H$ sao cho $W$ và $H$ chia hết cho $8$.
        - Đầu ra của mô hình bao gồm 2 phần chính:
            - **Interest Point Detector** dự đoán một **heatmap** có kích thước $W$ x $H$ với mỗi pixel là một giá trị trong khoảng $[0, 1]$. 
            **Heatmap** này được sử dụng để phát hiện keypoints trên ảnh đầu vào bằng cách chọn các điểm có giá trị lớn nhất trong **heatmap**.
            - **Descriptor Decoder** dự đoán một vector mô tả có kích thước $256$ cho mỗi keypoint được phát hiện.
        """
    )
