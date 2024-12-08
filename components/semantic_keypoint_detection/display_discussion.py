import os
import numpy as np
import cv2
import streamlit as st

images_name = os.listdir("services/semantic_keypoint_detection/tmp")


def generate_gaussian_pyramid(image, num_octaves, num_scales, sigma_base):
    gaussian_pyramid = []
    k = 2 ** (1 / 2)  # Factor to increase sigma
    for octave in range(num_octaves):
        gaussian_images = []
        for scale in range(num_scales + 3):  # Extra 3 scales for DoG computation
            sigma = sigma_base * (k**scale)
            if scale == 0 and octave == 0:
                # Original image for the first octave
                gaussian_images.append(cv2.GaussianBlur(image, (0, 0), sigma))
            elif scale == 0:
                # Downsample from the last image of the previous octave
                downsampled_image = cv2.resize(
                    gaussian_pyramid[octave - 1][-3], (0, 0), fx=0.5, fy=0.5
                )
                gaussian_images.append(
                    cv2.GaussianBlur(downsampled_image, (0, 0), sigma)
                )
            else:
                gaussian_images.append(
                    cv2.GaussianBlur(gaussian_images[0], (0, 0), sigma)
                )
        gaussian_pyramid.append(gaussian_images)
    return gaussian_pyramid


def compute_dog_pyramid(gaussian_pyramid):
    dog_pyramid = []
    for gaussian_images in gaussian_pyramid:
        dog_images = []
        for i in range(1, len(gaussian_images)):
            dog_images.append(gaussian_images[i] - gaussian_images[i - 1])
        dog_pyramid.append(dog_images)
    return dog_pyramid


sift = cv2.SIFT_create()
num_octaves = 4
num_scales = 5
sigma_base = 1.6


@st.fragment()
def display_discussion():
    st.header("5. Thảo luận")
    st.write("- **DoG** của một số hình ảnh trong tập dữ liệu:")

    for image_name in images_name:
        cols = st.columns(8)
        image = cv2.imread(f"services/semantic_keypoint_detection/tmp/{image_name}")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        kp = sift.detect(gray, None)
        _image = cv2.drawKeypoints(
            gray, kp, image.copy(), (0, 255, 0), cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG
        )

        gaussian_pyramid = generate_gaussian_pyramid(
            image, num_octaves, num_scales, sigma_base
        )
        dog_pyramid = compute_dog_pyramid(gaussian_pyramid)

        cols[0].image(_image, caption=f"{image_name}", use_column_width=True)
        for scale_idx, dog_image in enumerate(dog_pyramid[0]):
            cols[scale_idx + 1].image(
                dog_image, caption=f"Scale {scale_idx}", use_column_width=True
            )
    # st.write(
    #     """
    #     - Đối với $5$ loại hình **checkboard**, **cube**, **multiple polygon**, **polygon** và **star**:
    #         - Do **ORB** hoạt động tốt trong việc nhận diện các góc cạnh rõ ràng,
    #         điều này rất phổ biến trong $5$ loại hình đã đề cập ở trên
    #         (ví dụ: các ô vuông với điểm góc rõ ràng và đa giác với các cạnh sắc nét).
    #         - **SIFT** còn bị ảnh hưởng bởi các nhiễu trong background, hình vuông,
    #         tam giác ở $5$ loại hình trên (như trong hình 2.1.3.1).
    #     - Đổi với loại hình **stripes** và **lines**:
    #         - **ORB** thường phát hiện các keypoint dọc theo các cạnh
    #         (ví dụ như trong hình 2.2.3.3, 2.2.3.4 và 2.2.3.8),
    #         nhưng trong tập ground truth thì các có rất ít điểm keypoint nằm trên các đường thẳng này,
    #         vì thế **ORB** cho precision thấp trong loại hình này.
    #     """
    # )
