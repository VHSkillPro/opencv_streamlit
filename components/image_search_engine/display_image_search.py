import cv2
import numpy as np
from PIL import Image
import streamlit as st
from services.image_search_engine.services import search_image


@st.fragment()
def display_image_search():
    st.header("3. Tìm kiếm ảnh chứa đối tượng truy vấn")
    with st.form(key="form_image_search"):
        col1, col2 = st.columns([3, 1])
        uploaded_image = col1.file_uploader(
            "Chọn ảnh cần truy vấn", type=["jpg", "jpeg", "png"]
        )
        cnt_image_query = col2.number_input(
            "Số lượng ảnh dùng để truy vấn",
            min_value=1,
            value=100,
            step=1,
            max_value=5000,
        )
        image_number = col2.number_input(
            "Số lượng ảnh trả về", min_value=1, value=5, step=1, max_value=100
        )
        btn_submit = st.form_submit_button(":material/search: Tìm kiếm")

    if btn_submit:
        if uploaded_image is None:
            st.warning("Vui lòng chọn ảnh cần truy vấn!")
        else:
            mybar = st.progress(0)

            image = Image.open(uploaded_image)
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            with st.expander("Thông tin ảnh truy vấn"):
                st.write("Ảnh truy vấn:")
                st.image(image, use_column_width=True, channels="BGR")

            # Search for similar images
            results = search_image(image, image_number, cnt_image_query, mybar)
            cols = [st.columns(5) for _ in range(0, len(results), 5)]
            for i, result in enumerate(results):
                with cols[i // 5][i % 5]:
                    st.image(
                        result[0],
                        use_column_width=True,
                        channels="BGR",
                        caption=f"Ảnh {i+1} - Độ tương đồng: {result[1]:.4f}",
                    )
