import cv2
import streamlit as st

@st.fragment()
def display_colorspace_section(image: cv2.typing.MatLike):
    with st.form(key="colorspace_form"):
        colorspace = st.selectbox("Chọn không gian màu", ["RGB", "HSV", "GRAY"])
        submit = st.form_submit_button("Xử lý")
        
    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc (RGB)", use_container_width=True)
    
    if submit:
        colorspace_image = image.copy()
        if colorspace == "RGB":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2RGB)
        elif colorspace == "HSV":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2HSV)
        elif colorspace == "GRAY":
            colorspace_image = cv2.cvtColor(colorspace_image, cv2.COLOR_BGR2GRAY)
    
        cols[1].image(colorspace_image, "Ảnh sau khi biến đổi colorspace", use_container_width=True)
        
        