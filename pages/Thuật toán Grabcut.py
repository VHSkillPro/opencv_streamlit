import cv2
import numpy as np
from PIL import Image
import streamlit as st
from services.grabcut.grabcut import grabcut
from streamlit_drawable_canvas import st_canvas

st.set_page_config(
    page_title="Ứng dụng thuật toán GrabCut",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title("Ứng dụng thuật toán GrabCut")
uploaded_image = st.file_uploader(
    "Chọn hoặc kéo ảnh vào ô bên dưới", type=["jpg", "jpeg", "png"]
)

if uploaded_image is not None:
    st.write(":pencil: **Chọn vùng cần tách nền bằng cách kéo thả chuột trong ảnh**")
    st.write(":pencil: **Sau đó nhấn vào nút `Tách nền`**")
    submitBtn = st.button("Tách nền")

    cols = st.columns(2, gap="large")
    raw_image = Image.open(uploaded_image)

    with cols[0]:
        w, h = raw_image.size
        width = min(w, 475)
        height = width * h // w

        canvas_result = st_canvas(
            background_image=raw_image,
            drawing_mode="rect",
            fill_color="rgba(255, 165, 0, 0.1)",
            stroke_width=1,
            width=width,
            height=height,
        )

    if canvas_result.json_data is not None and submitBtn:
        if len(canvas_result.json_data.get("objects")) > 1:
            st.error("Chỉ được chọn một vùng cần tách nền")
        elif len(canvas_result.json_data.get("objects")) < 1:
            st.error("Vui lòng chọn một vùng cần tách nền")
        elif len(canvas_result.json_data.get("objects")) == 1:
            with st.spinner("Đang xử lý..."):
                orginal_image = np.array(raw_image)
                orginal_image = cv2.cvtColor(orginal_image, cv2.COLOR_RGBA2BGR)
                scale = orginal_image.shape[1] / width

                min_x = canvas_result.json_data.get("objects")[0]["left"]
                min_y = canvas_result.json_data.get("objects")[0]["top"]
                width = canvas_result.json_data.get("objects")[0]["width"]
                height = canvas_result.json_data.get("objects")[0]["height"]

                res = grabcut(
                    original_image=orginal_image,
                    rect=(
                        int(min_x * scale),
                        int(min_y * scale),
                        int(width * scale),
                        int(height * scale),
                    ),
                )

                cols[1].image(res, channels="BGR", caption="Ảnh kết quả")
