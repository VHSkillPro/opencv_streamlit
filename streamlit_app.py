import streamlit as st
import pages.grabcut_segmentation as grabcut_segmentation
import pages.watershed_segmentation as watershed_segmentation

page_map = {
    "grabcut_segmentation": {
        "page": grabcut_segmentation.page,
        "name": "Thuật toán Grabcut",
    },
    "watershed_segmentation": {
        "page": watershed_segmentation.page,
        "name": "Phân đoạn ký tự bằng Watershed Segmentation",
    },
}

input_page = st.sidebar.selectbox(
    "Chọn trang cần hiển thị",
    page_map.keys(),
    format_func=lambda page: page_map[page]["name"],
)

page_map[input_page]["page"]()
