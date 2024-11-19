import streamlit as st
from PIL import Image

from components.sort_mot.display_introduction import display_introduction
from components.sort_mot.display_method import display_method
from components.sort_mot.display_visualization import display_visualization

st.set_page_config(
    page_title="Thuật toán SORT (Simple Online and Realtime Tracking)",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Thuật toán SORT (Simple Online and Realtime Tracking)")
display_introduction()
display_method()
display_visualization()
