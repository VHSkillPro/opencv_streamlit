import cv2
import numpy as np
from PIL import Image
import streamlit as st
from components.image_search_engine import vectors, image_names
from sklearn.metrics.pairwise import cosine_similarity
from services.image_search_engine.services import VectorQuantization
from services.image_search_engine.superpoint import SuperPointFrontend

fe = SuperPointFrontend(
    weights_path="./services/image_search_engine/superpoint_v1.pth",
    nms_dist=4,
    conf_thresh=0.015,
    nn_thresh=0.7,
    cuda=True,
)

codebook = np.load("./services/image_search_engine/codebook.npy")
idf = np.load("./services/image_search_engine/idf.npy")
vq = VectorQuantization(codebook, idf)


@st.fragment()
def display_image_search():
    with st.form(key="form_image_search"):
        col1, col2 = st.columns([3, 1])
        uploaded_image = col1.file_uploader(
            "Chọn ảnh cần truy vấn", type=["jpg", "jpeg", "png"]
        )
        image_number = col2.number_input(
            "Số lượng ảnh trả về", min_value=1, value=5, step=1, max_value=100
        )
        btn_submit = st.form_submit_button(":material/search: Tìm kiếm")

    if btn_submit:
        if uploaded_image is None:
            st.warning("Vui lòng chọn ảnh cần truy vấn!")
        else:
            image = Image.open(uploaded_image)
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

            st.write("Ảnh truy vấn:")
            st.image(image, use_column_width=True, channels="BGR")

            gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray_scale = gray_scale.astype(np.float32) / 255.0
            _, desc, __ = fe.run(gray_scale)
            desc = desc.T

            query_vector = vq.transform(desc)
            scores = cosine_similarity([query_vector], vectors)
            topk = np.argsort(scores[0])[::-1][:image_number]

            st.write("Kết quả truy vấn:")
            cols = [st.columns(5) for _ in range(0, image_number, 5)]
            for i, idx in enumerate(topk):
                cols[i // 5][i % 5].image(
                    f"./services/image_search_engine/val2017/images/{image_names[idx]}",
                    caption=f"#{i + 1}",
                    use_column_width=True,
                )
