import streamlit as st
from PIL import Image

from components.tracking.display_introduction import display_introduction
from components.tracking.display_methods import display_methods
from components.tracking.display_visualization import display_visualization

st.set_page_config(
    page_title="Theo dõi đối tượng (SOT) bằng thuật toán KCF",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Theo dõi đối tượng (SOT) bằng thuật toán KCF")
display_introduction()
display_methods()
display_visualization()
