import cv2
import streamlit as st

@st.fragment()
def display_rotation_section(image: cv2.typing.MatLike):
    with st.form(key="roration_form"):
        theta = st.slider("Góc quay", -180, 180, 0)
        submit = st.form_submit_button("Xử lý")
        
    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)
    
    if submit:
        rotation_image = image.copy()
        
        h, w = rotation_image.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), theta, 1)
        rotation_image = cv2.warpAffine(rotation_image, M, (w, h), flags=cv2.INTER_LINEAR)
    
        cols[1].image(cv2.cvtColor(rotation_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi rotation", use_container_width=True)
        
        