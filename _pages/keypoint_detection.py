import streamlit as st
from PIL import Image
from components.semantic_keypoint_detection.display_datasets import display_datasets
from components.semantic_keypoint_detection.display_discussion import display_discussion
from components.semantic_keypoint_detection.display_evaluation import display_evaluation
from components.semantic_keypoint_detection.display_methods import display_methods
from components.semantic_keypoint_detection.display_results import display_results

st.set_page_config(
    page_title="Semantic Keypoint Detection bằng thuật toán SIFT và ORB",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Semantic Keypoint Detection bằng thuật toán SIFT và ORB")

display_datasets()
display_methods()
display_evaluation()
display_results()
display_discussion()
