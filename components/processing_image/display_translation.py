import cv2
import numpy as np
import streamlit as st

@st.fragment()
def display_translation_section(image: cv2.typing.MatLike):
    h, w = image.shape[:2]
    with st.form(key="translation_form"):
        cols = st.columns(2)
        tx = cols[0].number_input(f"Tịnh tiến theo chiều ngang trong đoạn [{-w}, {w}] (px)", min_value=-w, max_value=w, value=0)
        ty = cols[1].number_input(f"Tịnh tiến theo chiều dọc trong đoạn [{-h}, {h}] (px)", min_value=-h, max_value=h, value=0)
        submit = st.form_submit_button("Xử lý")
        
    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)
    
    if submit:
        translation_image = image.copy()
        translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
        translation_image = cv2.warpAffine(translation_image, translation_matrix, (w, h))
    
        cols[1].image(cv2.cvtColor(translation_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi tịnh tiến", use_container_width=True)
        
        