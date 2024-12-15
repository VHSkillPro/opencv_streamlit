from PIL import Image
import streamlit as st

st.set_page_config(
    page_title="Nhận dạng chữ viết tay",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.handwritting_letter_recognition.display_dataset import display_dataset
from components.handwritting_letter_recognition.display_method import display_method
from components.handwritting_letter_recognition.display_result import display_result
from components.handwritting_letter_recognition.display_discussion import (
    display_discussion,
)


st.title("Nhận dạng chữ viết tay")
display_dataset()
display_method()
display_result()
display_discussion()
