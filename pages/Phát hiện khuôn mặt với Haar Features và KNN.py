import cv2
import numpy as np
from PIL import Image
import streamlit as st

from services.face_detection.face_detection import detect_faces

st.set_page_config(
    page_title="Phát hiện khuôn mặt với Haar Features và KNN",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Phát hiện khuôn mặt với Haar Features và KNN")
uploaded_file = st.file_uploader("Chọn một file ảnh", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    faces = detect_faces(image)
    for x, y, w, h in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 2)

    st.image(image, channels="BGR")
