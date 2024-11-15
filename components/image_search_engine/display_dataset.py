import os
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

image_names = os.listdir("services/image_search_engine/val2017/images")


@st.fragment()
def display_dataset():
    st.header("1. Tập dữ liệu COCO")
    st.write(
        """
        - Tập dữ liệu **COCO (Common Objects in Context)** là một trong những tập dữ liệu phổ biến nhất cho bài toán nhận diện đối tượng.
        - Tập dữ liệu này chứa hơn $200.000$ ảnh và $1.5$ triệu nhãn cho $80$ loại đối tượng khác nhau.
        - Do kích thước quá lớn nên tập **val2017** chỉ chứa $5.000$ ảnh được chọn để sử dụng trong bài toán tìm kiếm ảnh chứa đối tượng truy vấn.
        - Một số ảnh trong tập **val2017**:
        """
    )
    for i in range(2):
        cols = st.columns(4)
        for j in range(4):
            cols[j].image(
                f"services/image_search_engine/val2017/images/{image_names[i * 4 + j]}",
                use_column_width=True,
            )

    image_sizes = np.load("services/image_search_engine/image_sizes.npy")
    w = [size[1] for size in image_sizes]
    h = [size[0] for size in image_sizes]

    st.write("- Biểu đồ thể hiện kích thước ảnh trong tập val2017:")
    fig, ax = plt.subplots()
    ax.scatter(w, h, s=3)
    ax.set_xlabel("Chiều rộng")
    ax.set_ylabel("Chiều cao")
    st.columns([1, 2, 1])[1].pyplot(fig)
