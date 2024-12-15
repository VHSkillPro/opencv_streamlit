import numpy as np
import streamlit as st
from components.handwritting_letter_recognition import test_phase


@st.fragment()
def display_discussion():
    st.header("4. Thảo luận")
    st.write("- Một số dự đoán sai của mô hình:")

    cnt_images = np.zeros(10, dtype=int)
    train_images_columns = [
        st.container().columns(21, vertical_alignment="center") for _ in range(10)
    ]
    labels, predicteds, images, __ = test_phase()

    for i in range(len(labels)):
        if labels[i] == predicteds[i]:
            continue

        if cnt_images[labels[i]] < 20:
            if cnt_images[labels[i]] == 0:
                train_images_columns[labels[i]][0].write(f"Act: {labels[i]}")
            train_images_columns[labels[i]][cnt_images[labels[i]] + 1].image(
                images[i].squeeze(), caption=f"Pred: {predicteds[i]}"
            )
            cnt_images[labels[i]] += 1
