import cv2, os
import PIL.Image as Image
import streamlit as st

__SERVICE_DIR = "./services/watershed_segmentation"

st.set_page_config(
    page_title="Ứng dụng Watershed Segmentation cho bài toán phân đoạn ký tự",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/labels/train/13xemay941.png")),
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/labels/train/2xemay103.png")),
]

test_labels = [
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/labels/test/1xemay1243.png")),
    cv2.imread(os.path.join(__SERVICE_DIR, "datasets/labels/test/2xemay1189.png")),
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
    channels="BGR",
)
cols[1].image(
    train_labels[1],
    caption="Ground truth của ảnh 2 trong tập train",
    use_column_width=True,
    channels="BGR",
)

cols[2].image(
    test_labels[0],
    caption="Ground truth của ảnh 1 trong tập test",
    use_column_width=True,
    channels="BGR",
)
cols[3].image(
    test_labels[1],
    caption="Ground truth của ảnh 2 trong tập test",
    use_column_width=True,
    channels="BGR",
)

st.header("2. Xác định tham số tối ưu")
