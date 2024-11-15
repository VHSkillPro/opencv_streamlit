from PIL import Image
import streamlit as st

from components.image_search_engine.display_methods import display_methods

st.set_page_config(
    page_title="Tìm kiếm ảnh chứa đối tượng truy vấn",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.image_search_engine.display_dataset import display_dataset
from components.image_search_engine.display_image_search import display_image_search

st.title("Tìm kiếm ảnh chứa đối tượng truy vấn")
display_dataset()
display_methods()
display_image_search()
