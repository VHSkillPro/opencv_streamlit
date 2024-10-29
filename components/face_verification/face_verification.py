import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from services.face_verification.sface import SFace
from services.face_verification.yunet import YuNet, detect_faces


@st.fragment()
def display_face_verification():
    st.header(":material/face: Xác thực khuôn mặt trong ảnh chân dung và thẻ sinh viên")
    with st.form(key="form_face_verification"):
        confThreshold = st.slider(
            "Chọn **confidence threshold** để phát hiện khuôn mặt", 0.0, 1.0, 0.85, 0.01
        )

        cols = st.columns(2)
        card = cols[0].file_uploader(
            "Chọn ảnh thẻ sinh viên", type=["jpg", "jpeg", "png"]
        )
        selfie = cols[1].file_uploader(
            "Chọn ảnh chân dung", type=["jpg", "jpeg", "png"]
        )
        btnVerify = st.form_submit_button(":material/check: Xác thực")

    if btnVerify:
        if (card is None) or (selfie is None):
            st.warning("Vui lòng chọn ảnh thẻ sinh viên và chân dung.")
        else:
            detector = YuNet(
                modelPath="./services/face_verification/models/face_detection_yunet_2023mar.onnx",
                confThreshold=confThreshold,
            )

            card = Image.open(card)
            card = ImageOps.exif_transpose(card)
            card = cv2.cvtColor(np.array(card), cv2.COLOR_RGB2BGR)
            card_face, card_scale = detect_faces(detector, card)

            if len(card_face) == 0:
                cols[0].error("Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên")
            elif len(card_face) > 1:
                cols[0].error("Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên")

            selfie = Image.open(selfie)
            selfie = ImageOps.exif_transpose(selfie)
            selfie = cv2.cvtColor(np.array(selfie), cv2.COLOR_RGB2BGR)
            selfie_face, selfie_scale = detect_faces(detector, selfie)

            if len(selfie_face) == 0:
                cols[1].error("Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên")
            elif len(selfie_face) > 1:
                cols[1].error("Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên")

            if len(card_face) == 1 and len(selfie_face) == 1:
                embedder = SFace(
                    "./services/face_verification/models/face_recognition_sface_2021dec.onnx"
                )

                card_h, card_w = card.shape[:2]
                scaled_card = cv2.resize(
                    card, (int(card_w * card_scale), int(card_h * card_scale))
                )
                selfie_h, selfie_w = selfie.shape[:2]
                scaled_selfie = cv2.resize(
                    selfie, (int(selfie_w * selfie_scale), int(selfie_h * selfie_scale))
                )

                score, match = embedder.match(
                    scaled_card, card_face[0], scaled_selfie, selfie_face[0]
                )

                _x, _y, _w, _h = map(lambda x: int(x / card_scale), card_face[0][:4])
                cv2.rectangle(
                    card,
                    (_x, _y),
                    (_x + _w, _y + _h),
                    (0, 255, 0) if match else (0, 0, 255),
                    2,
                )

                _x, _y, _w, _h = map(
                    lambda x: int(x / selfie_scale), selfie_face[0][:4]
                )
                cv2.rectangle(
                    selfie,
                    (_x, _y),
                    (_x + _w, _y + _h),
                    (0, 255, 0) if match else (0, 0, 255),
                    2,
                )

                with st.container(border=True):
                    st.write(f"**Confidence**: `{score}`")
                    cols = st.columns(2)
                    cols[0].image(
                        card,
                        caption="Ảnh thẻ sinh viên",
                        channels="BGR",
                        use_column_width=True,
                    )
                    cols[1].image(
                        selfie,
                        caption="Ảnh chân dung",
                        channels="BGR",
                        use_column_width=True,
                    )
