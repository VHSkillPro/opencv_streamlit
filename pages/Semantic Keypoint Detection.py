import streamlit as st
from PIL import Image
from components.semantic_keypoint_detection import (
    display_compare,
    display_datasets,
    display_result_ORB,
    display_result_SIFT,
)

st.set_page_config(
    page_title="Semantic Keypoint Detection",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("So sánh Semantic Keypoint Detection bằng SIFT và ORB")

display_datasets()
display_result_SIFT()
display_result_ORB()
display_compare()
