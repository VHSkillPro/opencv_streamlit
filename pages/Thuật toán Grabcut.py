import cv2, os
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

from services.grabcut.grabcut import grabcut

st.set_page_config(
    page_title="Ứng dụng thuật toán GrabCut",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Ứng dụng thuật toán GrabCut")

st.subheader("1. Chọn ảnh cần xử lý")
uploaded_image = st.file_uploader(
    "Chọn hoặc kéo ảnh vào ô bên dưới", type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:
    st.subheader("2. Chọn vùng cần xử lý bằng cách kéo chuột trên ảnh")
    cols = st.columns(2)

    with cols[0]:
        image = Image.open(uploaded_image)
        w, h = image.size

        st.columns(3)[1].write("Ảnh gốc")
        canvas_result = st_canvas(
            background_image=image,
            drawing_mode="rect",
            fill_color="rgba(255, 165, 0, 0.2)",
            stroke_width=1,
            width=400,
            height=400 * h // w,
        )

    with cols[1]:
        if canvas_result.json_data is not None:
            if len(canvas_result.json_data.get("objects")) > 1:
                st.error("Chỉ được chọn một vùng cần xử lý")
            elif len(canvas_result.json_data.get("objects")) == 1:
                st.columns(3)[1].write("Ảnh đã qua xử lý")

                orginal_image = np.array(image)
                orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_RGB2BGR)

                scale = w / 400
                min_x = canvas_result.json_data.get("objects")[0]["top"]
                min_y = canvas_result.json_data.get("objects")[0]["left"]
                height = canvas_result.json_data.get("objects")[0]["height"]
                width = canvas_result.json_data.get("objects")[0]["width"]

                res = grabcut(
                    original_image=orginal_image,
                    rect=(
                        int(min_x * scale),
                        int(min_y * scale),
                        int(width * scale),
                        int(height * scale),
                    ),
                )
                st.image(res, channels="BGR", width=400)
