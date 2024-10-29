import streamlit as st
from PIL import Image

from components.face_verification import init_session_state
from components.face_verification.class_manager import display_class_manager
from components.face_verification.face_verification import display_face_verification
from components.face_verification.student_manager import display_student_manager
from components.face_verification.student_verification import (
    display_student_verification,
)

init_session_state()

st.set_page_config(
    page_title="Ứng dụng xác nhận khuôn mặt",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

if len(st.session_state["toasts"]) > 0:
    for toast in st.session_state["toasts"]:
        st.toast(toast["body"], icon=toast["icon"])
    st.session_state["toasts"] = []

st.title("Ứng dụng xác nhận khuôn mặt")

display_class_manager()
display_student_manager()
display_face_verification()
display_student_verification()
