import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import streamlit as st
from services.face_verification.service import visualize
from services.face_verification.sface import SFace
from services.face_verification.db import StudentService
from services.face_verification.yunet import YuNet

__SERVICE_PATH__ = "services/face_verification"

studentService = StudentService()

backend_target_pairs = [
    [cv2.dnn.DNN_BACKEND_OPENCV, cv2.dnn.DNN_TARGET_CPU],
    [cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA],
    [cv2.dnn.DNN_BACKEND_CUDA, cv2.dnn.DNN_TARGET_CUDA_FP16],
    [cv2.dnn.DNN_BACKEND_TIMVX, cv2.dnn.DNN_TARGET_NPU],
    [cv2.dnn.DNN_BACKEND_CANN, cv2.dnn.DNN_TARGET_NPU],
]

backend_id, target_id = backend_target_pairs[0]

recognizer = SFace(
    modelPath=f"{__SERVICE_PATH__}/misc/face_recognition_sface_2021dec.onnx",
    disType=0,
    backendId=backend_id,
    targetId=target_id,
)

# ----------------------------------------------

if "submit_form" not in st.session_state:
    st.session_state["submit_form"] = False

if "show_form_add" not in st.session_state:
    st.session_state["show_form_add"] = False


@st.cache_data(ttl="1h")
def get_table_data():
    students = studentService.get_all()
    table_data = {"checkbox": [], "id": [], "card": [], "selfie": []}
    for id, student in students.items():
        table_data["checkbox"].append(False)
        table_data["id"].append(student["id"])
        table_data["card"].append(studentService.get_url_from_storage(student["card"]))
        table_data["selfie"].append(
            studentService.get_url_from_storage(student["selfie"], 3600)
        )
    return table_data


def display_table_students():
    table_data = get_table_data()
    if len(table_data["id"]) == 0:
        st.write("Không có sinh viên nào.")
        return pd.DataFrame(table_data)

    return st.data_editor(
        pd.DataFrame(table_data),
        column_config={
            "checkbox": st.column_config.CheckboxColumn("Chọn"),
            "id": st.column_config.TextColumn("Mã sinh viên", disabled=True),
            "card": st.column_config.ImageColumn("Thẻ sinh viên"),
            "selfie": st.column_config.ImageColumn("Chân dung"),
        },
        use_container_width=True,
        hide_index=True,
    )


def display_manage_students():
    def show_form_add():
        st.session_state["show_form_add"] = True
        st.session_state["submit_form"] = False

    def hide_form_add():
        st.session_state["show_form_add"] = False
        st.session_state["submit_form"] = False

    st.header("1. Danh sách sinh viên")
    container_action = st.container()
    container_form_add = st.container()
    data_editor = display_table_students()
    st.caption("- Click đúp vào ô ảnh cần xem để phóng to ảnh.")

    with container_action:
        cols = st.columns([1, 1, 8])
        with cols[0]:
            st.button("Thêm", use_container_width=True, on_click=show_form_add)
        with cols[1]:

            @st.dialog("Bạn có chắc chắn muốn xóa sinh viên đã chọn không?")
            def handle_remove_students():
                st.write("Danh sách sinh viên sẽ không thể khôi phục sau khi xóa.")
                st.write("Hãy chắc chắn trước khi xóa.")
                if st.button("Xác nhận"):
                    ids = data_editor[data_editor["checkbox"] == True]["id"].tolist()
                    haveChanges = False
                    for id in ids:
                        if studentService.delete(id):
                            haveChanges = True
                            st.toast(
                                f"Xóa sinh viên {id} thành công",
                                icon=":material/check:",
                            )
                        else:
                            st.toast(
                                f"Xóa sinh viên {id} thất bại", icon=":material/close:"
                            )

                    if haveChanges:
                        st.cache_data.clear()
                        st.rerun()

            if (data_editor["checkbox"] == True).sum() > 0:
                st.button(
                    "Xóa", use_container_width=True, on_click=handle_remove_students
                )

    if st.session_state["show_form_add"]:
        with container_form_add:
            with st.form("form_add"):
                st.markdown("#### Thêm sinh viên mới")
                id = st.text_input("Mã sinh viên")
                container_error_id = st.container()
                with container_error_id:
                    if st.session_state["submit_form"] and id.strip() == "":
                        st.caption(":red[Mã sinh viên không được để trống]")

                cols = st.columns(2)
                with cols[0]:
                    card = st.file_uploader("Thẻ sinh viên")
                    if st.session_state["submit_form"] and card is None:
                        st.caption(":red[Ảnh thẻ sinh viên không được để trống]")

                with cols[1]:
                    selfie = st.file_uploader("Chân dung")
                    if st.session_state["submit_form"] and selfie is None:
                        st.caption(":red[Ảnh chân dung không được để trống]")

                def handle_add():
                    st.session_state["submit_form"] = True
                    if id.strip() == "" or card is None or selfie is None:
                        return

                    isCreated = studentService.add(id, card, selfie)
                    if not isCreated:
                        container_error_id.caption(":red[Mã sinh viên đã tồn tại]")

                    st.cache_data.clear()
                    hide_form_add()
                    st.toast("Thêm sinh viên thành công", icon=":material/check:")
                    st.rerun()

                cols = st.columns([1, 1, 8])
                btn_submit = cols[0].form_submit_button(
                    "Thêm", use_container_width=True
                )
                cols[1].form_submit_button(
                    "Hủy", use_container_width=True, on_click=hide_form_add
                )

                if btn_submit:
                    handle_add()


def display_face_verification():
    st.header("2. Ứng dụng xác thực ảnh chân dung và thẻ sinh viên")
    with st.form("form_face_verification"):
        confThreshold = st.slider(
            "Chọn **confidence threshold** để phát hiện khuôn mặt", 0.0, 1.0, 0.9, 0.01
        )
        cols = st.columns(2)
        card = cols[0].file_uploader("Thẻ sinh viên")
        selfie = cols[1].file_uploader("Chân dung")
        btn_submit = st.form_submit_button("Xác thực")
        st.caption(
            """
                - Ảnh thẻ sinh viên và chân dung phải rõ ràng, không bị mờ.
                - Đảm bảo kích thước khuôn mặt trên ảnh thẻ sinh viên và chân dung nằm trong khoảng $10$x$10$ đến $300$x$300$ pixels.
            """
        )

    if btn_submit:
        if (card is None) or (selfie is None):
            st.warning("Vui lòng chọn ảnh thẻ sinh viên và chân dung.")
        else:
            detector = YuNet(
                modelPath=f"{__SERVICE_PATH__}/misc/face_detection_yunet_2023mar.onnx",
                confThreshold=confThreshold,
                nmsThreshold=0.3,
                topK=5000,
                backendId=backend_id,
                targetId=target_id,
            )

            card = Image.open(card)
            card = ImageOps.exif_transpose(card)
            card = cv2.cvtColor(np.array(card), cv2.COLOR_RGB2BGR)
            detector.setInputSize([card.shape[1], card.shape[0]])
            faces_card = detector.infer(card)
            if len(faces_card) == 0:
                st.warning(
                    "Không tìm thấy khuôn mặt trên thẻ sinh viên. Vui lòng chọn ảnh khác hoặc điều chỉnh **confidence threshold**."
                )

            selfie = Image.open(selfie)
            selfie = ImageOps.exif_transpose(selfie)
            selfie = cv2.cvtColor(np.array(selfie), cv2.COLOR_RGB2BGR)
            detector.setInputSize([selfie.shape[1], selfie.shape[0]])
            faces_selfie = detector.infer(selfie)
            if len(faces_selfie) == 0:
                st.warning(
                    "Không tìm thấy khuôn mặt trên ảnh chân dung. Vui lòng chọn ảnh khác hoặc điều chỉnh **confidence threshold**."
                )

            if len(faces_card) > 0 and len(faces_selfie) > 0:
                scores = []
                matches = []

                for face in faces_card:
                    result = recognizer.match(
                        selfie, faces_selfie[0][:-1], card, face[:-1]
                    )
                    scores.append(result[0])
                    matches.append(result[1])

                selfie, card = visualize(
                    selfie, faces_selfie, card, faces_card, matches, scores
                )

                cols = st.columns(2)
                cols[0].image(
                    selfie,
                    caption="Chân dung",
                    use_column_width=True,
                    channels="BGR",
                )
                cols[1].image(
                    card,
                    caption="Thẻ sinh viên",
                    use_column_width=True,
                    channels="BGR",
                )


# ----------------------------------------------

st.set_page_config(
    page_title="Face Verification",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Ứng dụng xác thực khuôn mặt")
display_manage_students()
display_face_verification()
