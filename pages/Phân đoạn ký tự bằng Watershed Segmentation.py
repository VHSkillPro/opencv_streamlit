import cv2, os
import numpy as np
import PIL.Image as Image
import streamlit as st
import pandas as pd

from services.watershed_segmentation.segmentation import (
    get_dice,
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
progress_bar = st.sidebar.progress(0, "Đang vẽ biểu đồ: 0%")

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
st.subheader("2.1. Tham số tối ưu")

cols = st.columns(2, gap="large")
cols[0].image(
    "./services/watershed_segmentation/iou.jpg",
    caption="Công thức IoU",
    use_column_width=True,
    channels="BGR",
)

cols[1].image(
    "./services/watershed_segmentation/dice_score.png",
    caption="Công thức Dice Score",
    use_column_width=True,
    channels="BGR",
)


@st.cache_data
def get_average(kernel: np.ndarray, thres: float) -> float:
    masks1 = license_plate_watershed_segmentation(train_images[0], kernel, thres)
    masks2 = license_plate_watershed_segmentation(train_images[1], kernel, thres)

    mask1 = get_mask_license_plate(masks1)
    mask2 = get_mask_license_plate(masks2)

    iou1 = get_iou(train_labels[0], mask1)
    iou2 = get_iou(train_labels[1], mask2)

    dice_1 = get_dice(train_labels[0], mask1)
    dice_2 = get_dice(train_labels[1], mask2)

    return ((iou1 + iou2) / 2, (dice_1 + dice_2) / 2)


def get_average_train(kernel_size: int) -> np.ndarray:
    global progress_bar_status

    iou = []
    dice = []

    for thres in np.linspace(0, 1, 100):
        (average_iou, average_dice) = get_average(
            (3 + 2 * kernel_size, 3 + 2 * kernel_size), thres
        )
        iou.append(average_iou)
        dice.append(average_dice)

        progress_bar_status += 1
        progress_bar.progress(
            progress_bar_status / 200,
            "Đang vẽ biểu đồ: " + str(progress_bar_status / 2) + "%",
        )

    return (iou, dice)


average_ious = [
    get_average_train(0),
    get_average_train(1),
]

cols = st.columns(2)

cols[0].write("Biểu đồ thể hiện average_iou trên tập train khi thay đổi thres")
cols[0].line_chart(
    {
        "thres": np.linspace(0, 1, 100),
        "kernel_size=3": average_ious[0][0],
        "kernel_size=5": average_ious[1][0],
    },
    x="thres",
    y=["kernel_size=3", "kernel_size=5"],
)

cols[1].write("Biểu đồ thể hiện average_dice_score trên tập train khi thay đổi thres")
cols[1].line_chart(
    {
        "thres": np.linspace(0, 1, 100),
        "kernel_size=3": average_ious[0][1],
        "kernel_size=5": average_ious[1][1],
    },
    x="thres",
    y=["kernel_size=3", "kernel_size=5"],
)

progress_bar.empty()

best = {
    "kernel_size": np.argmax([max(average_ious[0]), max(average_ious[1])]) * 2 + 3,
    "thres": np.argmax([average_ious[0], average_ious[1]]),
}


st.markdown(
    """
    Trong đó:
    - kernel_size là kích thước của tham số kernel
    - thres là ngưỡng để xác định true foreground
    - average_iou là giá trị trung bình của IoU trên tập train
    - average_dice_score là giá trị trung bình của Dice score trên tập train
    
    *Nhận xét*:
    - Tham số cho kết quả average_iou tốt nhất là kernel_size = {} và thres = {}
""".format(
        best["kernel_size"], best["thres"] / 100
    )
)

st.subheader("2.2. Minh hoạ mask của tập train theo từng tham số")

thres = st.slider("Chọn ngưỡng thres:", min_value=0.0, max_value=1.0, step=0.01)

cols = st.columns(4)
cols[0].image(
    train_images[0],
    caption="Ảnh 1 trong tập train",
    use_column_width=True,
    channels="BGR",
)

cols[1].image(
    train_labels[0],
    caption="Ground truth của ảnh 1 trong tập train",
    use_column_width=True,
)

masks = license_plate_watershed_segmentation(train_images[0], (3, 3), thres)
mask = get_mask_license_plate(masks)
cols[2].image(
    mask,
    caption="Mask của ảnh 1 trong tập train với kernel_size = 3, IoU = {:.5f} và Dice Score = {:.5f}".format(
        get_iou(train_labels[0], mask), get_dice(train_labels[0], mask)
    ),
)

masks = license_plate_watershed_segmentation(train_images[0], (5, 5), thres)
mask = get_mask_license_plate(masks)
cols[3].image(
    mask,
    caption="Mask của ảnh 1 trong tập train với kernel_size = 5, IoU = {:.5f} và Dice Score = {:.5f}".format(
        get_iou(train_labels[0], mask), get_dice(train_labels[0], mask)
    ),
)

cols = st.columns(4)
cols[0].image(
    train_images[1],
    caption="Ảnh 2 trong tập train",
    use_column_width=True,
    channels="BGR",
)

cols[1].image(
    train_labels[1],
    caption="Ground truth của ảnh 2 trong tập train",
    use_column_width=True,
)

masks = license_plate_watershed_segmentation(train_images[1], (3, 3), thres)
mask = get_mask_license_plate(masks)
cols[2].image(
    mask,
    caption="Mask của ảnh 2 trong tập train với kernel_size = 3, IoU = {:.5f} và Dice Score = {:.5f}".format(
        get_iou(train_labels[1], mask), get_dice(train_labels[1], mask)
    ),
)

masks = license_plate_watershed_segmentation(train_images[1], (5, 5), thres)
mask = get_mask_license_plate(masks)
cols[3].image(
    mask,
    caption="Mask của ảnh 2 trong tập train với kernel_size = 5, IoU = {:.5f} và Dice Score = {:.5f}".format(
        get_iou(train_labels[1], mask), get_dice(train_labels[1], mask)
    ),
)

st.header("3. Kết quả phân đoạn ký tự trên tập test")

cols = st.columns(3)
cols[0].image(
    test_images[0],
    caption="Ảnh 1 trong tập test",
    use_column_width=True,
    channels="BGR",
)
cols[1].image(
    test_labels[0],
    caption="Ground truth của ảnh 1 trong tập test",
    use_column_width=True,
)

mask = get_mask_license_plate(
    license_plate_watershed_segmentation(
        test_images[0],
        (int(best["kernel_size"]), int(best["kernel_size"])),
        best["thres"],
    )
)
cols[2].image(
    mask,
    caption="Mask của ảnh 1 trong tập test với kernel_size = {}, thres = {} và IoU = {:.5f} và Dice Score = {:.5f} ".format(
        best["kernel_size"],
        best["thres"] / 100,
        get_iou(test_labels[0], mask),
        get_dice(test_labels[0], mask),
    ),
    use_column_width=True,
)

cols = st.columns(3)
cols[0].image(
    test_images[1],
    caption="Ảnh 2 trong tập test",
    use_column_width=True,
    channels="BGR",
)
cols[1].image(
    test_labels[1],
    caption="Ground truth của ảnh 2 trong tập test",
    use_column_width=True,
)

mask = get_mask_license_plate(
    license_plate_watershed_segmentation(
        test_images[1],
        (int(best["kernel_size"]), int(best["kernel_size"])),
        best["thres"],
    )
)
cols[2].image(
    mask,
    caption="Mask của ảnh 2 trong tập test với kernel_size = {}, thres = {} và IoU = {:.5f} và Dice Score = {:.5f} ".format(
        best["kernel_size"],
        best["thres"] / 100,
        get_iou(test_labels[1], mask),
        get_dice(test_labels[1], mask),
    ),
    use_column_width=True,
)
