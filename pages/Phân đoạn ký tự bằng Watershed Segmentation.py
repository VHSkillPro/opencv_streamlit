import cv2, os
import numpy as np
import PIL.Image as Image
import streamlit as st

from services.watershed_segmentation.segmentation import (
    get_iou,
    get_mask_license_plate,
    license_plate_watershed_segmentation,
)

__SERVICE_DIR = "./services/watershed_segmentation"

st.set_page_config(
    page_title="Ứng dụng Watershed Segmentation cho bài toán phân đoạn ký tự",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

progress_bar_status = 0
progress_bar = st.sidebar.progress(0)

st.title("Ứng dụng Watershed Segmentation cho bài toán phân đoạn ký tự")
st.header("1. Tập dữ liệu")
st.write(
    "- Tập dữ liệu bao gồm 4 ảnh chia thành hai tập train và tập test, mỗi tập gồm 2 ảnh."
)

train_images = [
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/images/train/13xemay941.jpg")),
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/images/train/2xemay103.jpg")),
]

test_images = [
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/images/test/1xemay1243.jpg")),
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/images/test/2xemay1189.jpg")),
]

train_labels = [
    cv2.imread(
        os.path.join(__SERVICE_DIR, "datasets/labels/train/13xemay941.png"),
        cv2.IMREAD_GRAYSCALE,
    ),
    cv2.imread(
        os.path.join(__SERVICE_DIR, "datasets/labels/train/2xemay103.png"),
        cv2.IMREAD_GRAYSCALE,
    ),
]

test_labels = [
    cv2.imread(
        os.path.join(__SERVICE_DIR, "datasets/labels/test/1xemay1243.png"),
        cv2.IMREAD_GRAYSCALE,
    ),
    cv2.imread(
        os.path.join(__SERVICE_DIR, "datasets/labels/test/2xemay1189.png"),
        cv2.IMREAD_GRAYSCALE,
    ),
]

# Display images
cols = st.columns(4)
cols[0].image(
    train_images[0],
    caption="Ảnh 1 trong tập train",
    use_column_width=True,
    channels="BGR",
)
cols[1].image(
    train_images[1],
    caption="Ảnh 2 trong tập train",
    use_column_width=True,
    channels="BGR",
)

cols[2].image(
    test_images[0],
    caption="Ảnh 1 trong tập test",
    use_column_width=True,
    channels="BGR",
)
cols[3].image(
    test_images[1],
    caption="Ảnh 2 trong tập test",
    use_column_width=True,
    channels="BGR",
)

# Display ground truth
cols = st.columns(4)
cols[0].image(
    train_labels[0],
    caption="Ground truth của ảnh 1 trong tập train",
    use_column_width=True,
)
cols[1].image(
    train_labels[1],
    caption="Ground truth của ảnh 2 trong tập train",
    use_column_width=True,
)

cols[2].image(
    test_labels[0],
    caption="Ground truth của ảnh 1 trong tập test",
    use_column_width=True,
)
cols[3].image(
    test_labels[1],
    caption="Ground truth của ảnh 2 trong tập test",
    use_column_width=True,
)

st.header("2. Xác định tham số tối ưu")

cols = st.columns(2)
for i in range(2):
    average_iou = []

    cols[i].write(
        "Biểu đồ thể hiện average_iou trên tập train khi thay đổi thres và kernel_size = "
        + str(3 + i * 2)
    )

    for thres in np.linspace(0, 0.1, 100):
        masks1 = license_plate_watershed_segmentation(
            train_images[0], (3 + i * 2, 3 + i * 2), thres
        )
        masks2 = license_plate_watershed_segmentation(
            train_images[1], (3 + i * 2, 3 + i * 2), thres
        )

        mask1 = get_mask_license_plate(masks1)
        mask2 = get_mask_license_plate(masks2)

        iou1 = get_iou(train_labels[0], mask1)
        iou2 = get_iou(train_labels[1], mask2)

        average_iou.append((iou1 + iou2) / 2)

        progress_bar_status += 1
        progress_bar.progress(progress_bar_status / 200)

    cols[i].line_chart(average_iou)

progress_bar.empty()
