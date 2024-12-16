from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Ứng dụng xử lý ảnh",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.processing_image.display_app import display_app

st.title("Ứng dụng xử lý ảnh")
display_app()