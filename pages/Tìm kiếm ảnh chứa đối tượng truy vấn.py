import streamlit as st
from PIL import Image
from components.image_search_engine.display_image_search import display_image_search

st.set_page_config(
    page_title="Tìm kiếm ảnh chứa đối tượng truy vấn",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Tìm kiếm ảnh chứa đối tượng truy vấn")

display_image_search()
