import streamlit as st
from PIL import Image
from components.keypoint_matching.display_dataset import display_dataset
from components.keypoint_matching.display_discussion import display_discussion
from components.keypoint_matching.display_evaluation import display_evaluation
from components.keypoint_matching.display_methods import display_methods
from components.keypoint_matching.display_result import display_result

st.set_page_config(
    page_title="Semantic Keypoint Detection bằng thuật toán SIFT và ORB",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title(
    "Đánh giá Matching Keypoint bằng SIFT, ORB và SuperPoint trên tiêu chí Rotation"
)

display_dataset()
display_methods()
display_evaluation()
display_result()
display_discussion()
