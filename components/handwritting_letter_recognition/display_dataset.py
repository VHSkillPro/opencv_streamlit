import numpy as np
import streamlit as st
from torchvision import datasets, transforms

transform = transforms.Compose([transforms.ToTensor()])
train_dataset = datasets.MNIST(
    root="services/handwriting_letter_recognition",
    train=True,
    download=True,
    transform=transform,
)


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
        - Một số ảnh trong bộ dữ liệu **MNIST**:
        """
    )

    train_images_columns = [st.container().columns(31) for _ in range(10)]
    cnt_images = np.zeros(10, dtype=int)
    for image, label in train_dataset:
        if cnt_images[label] < 30:
            if cnt_images[label] == 0:
                train_images_columns[label][0].write(label)
            train_images_columns[label][cnt_images[label] + 1].image(
                image.squeeze(0).cpu().numpy()
            )
            cnt_images[label] += 1
        if np.sum(cnt_images) == 300:
            break
