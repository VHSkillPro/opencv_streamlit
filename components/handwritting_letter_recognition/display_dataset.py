import numpy as np


def dummy_npwarn_decorator_factory():
    def npwarn_decorator(x):
        return x

    return npwarn_decorator


np._no_nep50_warning = getattr(np, "_no_nep50_warning", dummy_npwarn_decorator_factory)

import streamlit as st
import matplotlib.pyplot as plt
import keras

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_val, y_val = X_train[50000:60000, :], y_train[50000:60000]
X_train, y_train = X_train[:50000, :], y_train[:50000]


@st.fragment()
def display_dataset():
    st.header("1. MNIST Dataset")
    st.write(
        """
        - **MNIST** là một trong những bộ dữ liệu nổi tiếng và phổ biến nhất trong cộng đồng học máy, 
        đặc biệt là trong các nghiên cứu về nhận diện mẫu và phân loại hình ảnh.
        - **MNIST** bao gồm $70.000$ ảnh chữ số viết tay từ $0$ đến $9$, mỗi ảnh có kích thước $28$ x $28$ pixel, bao gồm:
            - Training set gồm $60.000$ ảnh.
            - Test set gồm $10.000$ ảnh.
        - Mỗi hình ảnh là một chữ số viết tay được chụp lại và chuyển thành dạng ảnh **grayscale** (ảnh đen trắng).
        - Các chữ số trong bộ dữ liệu **MNIST** đã được chuẩn hóa và canh chỉnh kích thước để phù hợp với việc huấn luyện mô hình.
        """
    )

    st.subheader("1.1. Một số ảnh trong training set")
    train_images = []
    train_labels = []
    for i, label in enumerate(y_train):
        if label not in train_labels:
            train_images.append(i)
            train_labels.append(label)
        if len(train_images) == 10:
            break

    train_images_cols = st.columns(10)
    for i in range(10):
        id = train_images[i]
        train_images_cols[i].image(
            X_train[id], caption=f"Label: {y_train[id]}", use_container_width=True
        )

    st.subheader("1.2. Một số ảnh trong test set")
    test_images = []
    test_labels = []
    for i, label in enumerate(y_test):
        if label not in test_labels:
            test_images.append(i)
            test_labels.append(label)
        if len(test_images) == 10:
            break

    test_images_cols = st.columns(10)
    for i in range(10):
        id = test_images[i]
        test_images_cols[i].image(
            X_test[id], caption=f"Label: {y_test[id]}", use_container_width=True
        )
