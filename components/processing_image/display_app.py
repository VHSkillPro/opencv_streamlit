import cv2
import numpy as np
import streamlit as st
from components.processing_image.display_colorspace import display_colorspace_section
from components.processing_image.display_cropping import display_cropping_section
from components.processing_image.display_flip import display_flip_section
from components.processing_image.display_rotation import display_rotation_section
from components.processing_image.display_translation import display_translation_section

@st.fragment()
def display_app():
    st.write(
        """
        - Ứng dụng này giúp bạn thực hiện các kỹ thuật xử lý ảnh cơ bản như: **Flip**, **Rotation**, **Colorspace**, **Translation**, **Cropping**.
        - Vui lòng chọn kỹ thuật cần thực hiện và tải ảnh lên để xử lý.
        """
    )
    
    with st.container(border=True):
        technique = st.selectbox("Chọn kỹ thuật cần thực hiện", ["Flip", "Rotation", "Colorspace", "Translation", "Cropping"])
        uploaded_image = st.file_uploader("Chọn một ảnh cần xử lý", type=["jpg", "png"], accept_multiple_files=False)
    
    if uploaded_image is not None:
        switcher = {
            "flip": display_flip_section,
            "rotation": display_rotation_section,
            "colorspace": display_colorspace_section,
            "translation": display_translation_section,
            "cropping": display_cropping_section
        }
        
        file_bytes = np.asarray(bytearray(uploaded_image.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if technique.lower() in switcher:
            switcher[technique.lower()](image)
        else:
            st.write("Tính năng đang phát triển")
