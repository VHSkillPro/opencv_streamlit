import cv2
import streamlit as st

@st.fragment()
def display_flip_section(image: cv2.typing.MatLike):
    with st.form(key="flip_form"):
        flip_options = ["Horizontal", "Vertical", "Both"]
        flip_option = st.selectbox("Chọn hướng flip", flip_options)
        submit = st.form_submit_button("Xử lý")
        
    cols = st.columns(2)
    cols[0].image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), "Ảnh gốc", use_container_width=True)
    
    if submit:
        flip_image = image.copy()
        if flip_option == "Vertical":
            flip_image = cv2.flip(flip_image, 0)
        elif flip_option == "Horizontal":
            flip_image = cv2.flip(flip_image, 1)
        else:
            flip_image = cv2.flip(flip_image, -1)
            
        cols[1].image(cv2.cvtColor(flip_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi flip", use_container_width=True)
        
        