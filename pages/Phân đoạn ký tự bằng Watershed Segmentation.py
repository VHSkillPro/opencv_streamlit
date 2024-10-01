import cv2, os
import numpy as np
import pandas as pd
import streamlit as st
from pathlib import Path
import PIL.Image as Image

from services.watershed_segmentation.segmentation import (
    get_dice_score,
    get_iou,
    get_mask_license_plate,
    license_plate_watershed_segmentation,
)

__SERVICE_DIR = "./services/watershed_segmentation"
__IMAGES_DIR = os.path.join(__SERVICE_DIR, "datasets/images")
__LABELS_DIR = os.path.join(__SERVICE_DIR, "datasets/labels")

train_images_name = os.listdir(os.path.join(__IMAGES_DIR, "train"))
test_images_name = os.listdir(os.path.join(__IMAGES_DIR, "test"))

train_images, train_labels = [], []
for image_name in train_images_name:
    train_images.append(cv2.imread(os.path.join(__IMAGES_DIR, "train", image_name)))
    label_name = Path(image_name).stem + ".png"
    train_labels.append(
        cv2.imread(
            os.path.join(__LABELS_DIR, "train", label_name), cv2.IMREAD_GRAYSCALE
        )
    )

test_images, test_labels = [], []
for image_name in test_images_name:
    test_images.append(cv2.imread(os.path.join(__IMAGES_DIR, "test", image_name)))
    label_name = Path(image_name).stem + ".png"
    test_labels.append(
        cv2.imread(os.path.join(__LABELS_DIR, "test", label_name), cv2.IMREAD_GRAYSCALE)
    )

# Load average ious and calc best param iou
df = pd.read_csv(os.path.join(__SERVICE_DIR, "average_ious.csv"))
average_ious = df.to_numpy()[:, 1:].T

best_param_iou = {
    "kernel_size": 2
    * np.argmax(max(average_ious[i]) for i in range(average_ious.shape[0]))
    + 3,
    "thres": (np.argmax(average_ious) % average_ious.shape[1]) / average_ious.shape[1],
}

# Load average dices and calc best param dice
df = pd.read_csv(os.path.join(__SERVICE_DIR, "average_dices.csv"))
average_dices = df.to_numpy()[:, 1:].T

best_param_dice = {
    "kernel_size": 2
    * np.argmax(max(average_dices[i]) for i in range(average_dices.shape[0]))
    + 3,
    "thres": (np.argmax(average_dices) % average_dices.shape[1])
    / average_dices.shape[1],
}

# ----------------------------------------------------------


def display_datasets():
    st.header("1. Tập dữ liệu")
    st.write(
        "- Tập dữ liệu bao gồm $4$ ảnh chia thành hai tập bao gồm tập train và tập test, mỗi tập gồm $2$ ảnh."
    )

    cols = st.columns(2)
    with cols[0]:
        st.subheader("1.1. Tập train")
        sub_cols = st.columns(2)

        for i in range(2):
            sub_cols[i].image(
                train_images[i],
                caption=f"Ảnh {i+1} trong tập train",
                use_column_width=True,
                channels="BGR",
            )
            sub_cols[i].image(
                train_labels[i],
                caption=f"Ground truth của ảnh {i+1} trong tập train",
                use_column_width=True,
            )

    with cols[1]:
        st.subheader("1.2. Tập test")
        sub_cols = st.columns(2)

        for i in range(2):
            sub_cols[i].image(
                test_images[i],
                caption=f"Ảnh {i+1} trong tập test",
                use_column_width=True,
                channels="BGR",
            )
            sub_cols[i].image(
                test_labels[i],
                caption=f"Ground truth của ảnh {i+1} trong tập test",
                use_column_width=True,
            )


def display_tranning_process():
    st.header("2. Quá trình huấn luyện")

    def display_pipline():
        st.subheader("2.1. Quá trình phân đoạn ký tự bằng Watershed Segmentation")

    def display_metrics():
        st.subheader("2.2. Độ đo IoU và Dice Score")

        st.markdown(
            """
            - IoU là một độ đo phổ biến để đánh giá mức độ chồng lấn giữa hai vùng trong ảnh, 
            được tính bằng cách chia diện tích phần giao của hai hình cho diện tích phần hợp của hai hình đó.
            - Dice Score là một độ đo phổ biến được sử dụng để đánh giá mức độ tương đồng giữa hai tập hợp, 
            được tính bằng cách lấy tổng số phần tử của phần giao của hai tập hợp chia cho tổng số phần tử của cả hai tập hợp.
            """
        )
        st.columns([1, 2, 1])[1].image(
            os.path.join(__SERVICE_DIR, "iou_vs_dice.png"),
            use_column_width=True,
            caption="Công thức IoU và Dice Score (Dice Coefficient)",
        )

    def display_hyperparameters():
        st.subheader("2.3. Tham số tối ưu")
        cols = st.columns(2, gap="medium")

        with cols[0]:
            st.markdown("#### 2.3.1. Tham số tối ưu theo IoU")
            st.write("- Biểu đồ thể hiện Average IoU trên tập train khi thay đổi thres")

            st.line_chart(
                {
                    "thres": np.linspace(0, 1, average_ious.shape[1]),
                    "kernel_size = 3": average_ious[0],
                    "kernel_size = 5": average_ious[1],
                    "kernel_size = 7": average_ious[2],
                    "kernel_size = 9": average_ious[3],
                },
                x="thres",
                y=[
                    "kernel_size = 3",
                    "kernel_size = 5",
                    "kernel_size = 7",
                    "kernel_size = 9",
                ],
                y_label="Average IoU",
            )

            st.markdown(
                """
                - Average IoU tốt nhất: ${:.6f}$
                - Tham số cho kết quả Average IoU tốt nhất là:
                    - kernel_size = ${}$
                    - thres = ${:.6f}$
                """.format(
                    np.max(average_ious),
                    best_param_iou["kernel_size"],
                    best_param_iou["thres"],
                )
            )

        with cols[1]:
            st.markdown("#### 2.3.2. Tham số tối ưu theo DICE")
            st.write(
                "- Biểu đồ thể hiện Average DICE trên tập train khi thay đổi thres"
            )

            st.line_chart(
                {
                    "thres": np.linspace(0, 1, average_dices.shape[1]),
                    "kernel_size = 3": average_dices[0],
                    "kernel_size = 5": average_dices[1],
                    "kernel_size = 7": average_dices[2],
                    "kernel_size = 9": average_dices[3],
                },
                x="thres",
                y=[
                    "kernel_size = 3",
                    "kernel_size = 5",
                    "kernel_size = 7",
                    "kernel_size = 9",
                ],
                y_label="Average DICE",
            )

            st.markdown(
                """
                - Average DICE tốt nhất: ${:.6f}$
                - Tham số cho kết quả Average DICE tốt nhất là:
                    - kernel_size = ${}$
                    - thres = ${:.6f}$
                """.format(
                    np.max(average_dices),
                    best_param_dice["kernel_size"],
                    best_param_dice["thres"],
                )
            )

    def display_visualize():
        st.subheader("2.4. Minh hoạ mask của tập train theo từng bộ tham số")
        cols = st.columns([1, 2], gap="medium")
        kernel_size = cols[0].selectbox(
            "Chọn kernel_size:", (3, 5, 7, 9), format_func=lambda x: f"{x} x {x}"
        )
        thres = cols[1].slider(
            "Chọn thres:", min_value=0.0, max_value=1.0, step=1 / 500
        )

        cols = st.columns(4)
        cols[0].columns([2, 2, 1])[1].write("**Ảnh gốc**")
        cols[1].columns([1, 2, 1])[1].write("**Ground truth**")
        cols[2].columns([2, 2, 1])[1].write("**Mask**")
        cols[3].columns([2, 2, 1])[1].write("**Thông số**")

        for i in range(2):
            cols = st.columns(4, vertical_alignment="center")

            with cols[0]:
                st.image(
                    train_images[i],
                    caption=f"Ảnh {i+1} trong tập train",
                    use_column_width=True,
                    channels="BGR",
                )

            with cols[1]:
                st.image(
                    train_labels[i],
                    caption=f"Ground truth của ảnh {i+1} trong tập train",
                    use_column_width=True,
                )

            with cols[2]:
                masks = license_plate_watershed_segmentation(
                    train_images[i], kernel_size, thres
                )
                mask = get_mask_license_plate(masks)
                _mask = mask.copy()
                _mask[_mask == 1] = 255
                st.image(_mask, caption=f"Mask của ảnh {i+1} trong tập train")

            with cols[3]:
                _label = np.copy(train_labels[i])
                _label[_label == 255] = 1
                st.markdown(
                    """
                    - IoU: ${:.6f}$
                    - Dice Score: ${:.6f}$
                    """.format(
                        get_iou(_label, mask),
                        get_dice_score(_label, mask),
                    )
                )

    display_pipline()
    display_metrics()
    display_hyperparameters()
    display_visualize()


def display_result():
    st.header("3. Kết quả phân đoạn ký tự trên tập test")

    cols = st.columns(5)
    cols[0].columns([2, 2, 1])[1].write("**Ảnh gốc**")
    cols[1].columns([1, 2, 1])[1].write("**Ground truth**")
    cols[2].columns([1, 2, 1])[1].write("**Mask theo IoU**")
    cols[3].columns([1, 2, 1])[1].write("**Mask theo DICE**")
    cols[4].columns([2, 2, 1])[1].write("**Thông số**")

    for i in range(len(test_images)):
        cols = st.columns(5, vertical_alignment="center")

        with cols[0]:
            st.image(
                test_images[i],
                caption=f"Ảnh {i+1} trong tập test",
                use_column_width=True,
                channels="BGR",
            )

        with cols[1]:
            st.image(
                test_labels[i],
                caption=f"Ground truth của ảnh {i+1} trong tập test",
                use_column_width=True,
            )

        with cols[2]:
            masks = license_plate_watershed_segmentation(
                test_images[i],
                int(best_param_iou["kernel_size"]),
                best_param_iou["thres"],
            )
            mask = get_mask_license_plate(masks)
            _mask = mask.copy()
            _mask[_mask == 1] = 255
            st.image(
                _mask,
                caption=f"Mask theo IoU của ảnh {i+1} trong tập test",
                use_column_width=True,
            )
            _label = np.copy(test_labels[i])
            _label[_label == 255] = 1
            iou = get_iou(_label, mask)

        with cols[3]:
            masks = license_plate_watershed_segmentation(
                test_images[i],
                int(best_param_dice["kernel_size"]),
                best_param_dice["thres"],
            )
            mask = get_mask_license_plate(masks)
            _mask = mask.copy()
            _mask[_mask == 1] = 255
            st.image(
                _mask,
                caption=f"Mask theo DICE của ảnh {i+1} trong tập test",
                use_column_width=True,
            )
            _label = np.copy(test_labels[i])
            _label[_label == 255] = 1
            dice = get_dice_score(_label, mask)

        with cols[4]:
            st.markdown(
                """
                - IoU: ${:.6f}$
                - Dice Score: ${:.6f}$
                """.format(
                    iou,
                    dice,
                )
            )


# ----------------------------------------------------------

st.set_page_config(
    page_title="Ứng dụng Watershed Segmentation cho bài toán phân đoạn ký tự",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Ứng dụng Watershed Segmentation cho bài toán phân đoạn ký tự")

display_datasets()
display_tranning_process()
display_result()
