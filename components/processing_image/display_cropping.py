import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas, CanvasResult

def display_st_canvas(raw_image: cv2.typing.MatLike):
    h, w = raw_image.shape[:2]
    width = min(w, 475)
    height = width * h // w
    ratio = width / w

    mode = "rect"
    stroke_color = "rgb(255, 0, 0)"
    stroke_width = 2
    
    canvas_result = st_canvas(
        background_image=Image.fromarray(cv2.cvtColor(raw_image, cv2.COLOR_BGR2RGB)),
        drawing_mode=mode,
        fill_color="rgba(0, 0, 0, 0)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        width=width + 1,
        height=height + 1,
        key="full_app",
    )

    return canvas_result, ratio

@st.fragment()
def display_cropping_section(image: cv2.typing.MatLike):
    cols = st.columns(2)
    with cols[0]:
        canvas_result, ratio = display_st_canvas(image)
    
    objects = None
    if canvas_result is not None and canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        
    if objects is None or len(objects) == 0:
        st.warning("Vui lòng chọn vùng cần cropping")
    elif len(objects) > 1:
        st.warning("Chỉ chọn một vùng cần cropping")
    else:
        x1, y1, x2, y2 = objects[0]["left"], objects[0]["top"], objects[0]["left"] + objects[0]["width"], objects[0]["top"] + objects[0]["height"]
        x1 = int(x1 / ratio)
        y1 = int(y1 / ratio)
        x2 = int(x2 / ratio)
        y2 = int(y2 / ratio)
        cropped_image = image.copy()
        cropped_image = cropped_image[y1:y2, x1:x2]
        cols[1].image(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB), "Ảnh sau khi cắt", use_container_width=True)
        