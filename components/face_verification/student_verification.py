import cv2
import numpy as np
import streamlit as st
from PIL import Image, ImageOps
from services.face_verification.sface import SFace
from services.face_verification.yunet import YuNet
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching


@st.fragment()
def display_student_verification():
    with st.form(key="form_student_verification"):
        confThreshold = st.slider(
            "Chọn **confidence threshold** để phát hiện khuôn mặt", 0.0, 1.0, 0.85, 0.01
        )
        img = st.file_uploader("Chọn ảnh lớp học", type=["jpg", "jpeg", "png"])
        btnVerify = st.form_submit_button(":material/check: Xác thực")

    if btnVerify:
        with st.container(border=True):
            if img is None:
                st.warning("Vui lòng chọn ảnh lớp học.")
            else:
                detector = YuNet(
                    modelPath="./services/face_verification/models/face_detection_yunet_2023mar.onnx",
                    confThreshold=confThreshold,
                )

                img = Image.open(img)
                img = ImageOps.exif_transpose(img)
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                detector.setInputSize([img.shape[1], img.shape[0]])
                faces = detector.infer(img)

                if len(faces) > 0:
                    embedder = SFace(
                        "./services/face_verification/models/face_recognition_sface_2021dec.onnx"
                    )

                    match_matrix = np.zeros(
                        (len(faces), len(st.session_state["face_labels"]))
                    )
                    score_matrix = np.zeros(
                        (len(faces), len(st.session_state["face_labels"]))
                    )
                    for i, face in enumerate(faces):
                        feature = embedder.infer(img, face)
                        for j, face_features in enumerate(
                            st.session_state["card_face_features"]
                        ):
                            score, match = embedder.match_feature(
                                feature,
                                np.array(
                                    [face_features], dtype=np.dtype(feature[0][0])
                                ),
                            )
                            match_matrix[i][j] = match
                            score_matrix[i][j] = score

                    idx = maximum_bipartite_matching(
                        csr_matrix(match_matrix), perm_type="column"
                    )

                    cnt = 0
                    cols = st.columns(6)
                    for i, id in enumerate(idx):
                        _x, _y, _w, _h = map(int, faces[i][:4])
                        if id == -1:
                            cv2.rectangle(
                                img, (_x, _y), (_x + _w, _y + _h), (0, 0, 255), 2
                            )
                        else:
                            cols[cnt].image(
                                img[_y : _y + _h, _x : _x + _w],
                                channels="BGR",
                                use_column_width=True,
                                caption=st.session_state["face_names"][id],
                            )

                            cv2.rectangle(
                                img, (_x, _y), (_x + _w, _y + _h), (0, 255, 0), 2
                            )
                            cv2.putText(
                                img,
                                st.session_state["face_labels"][id],
                                (_x, _y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.9,
                                (0, 255, 0),
                                2,
                            )

                            cnt = (cnt + 1) % 6
                            if cnt == 0:
                                cols = st.columns(6)

                st.image(img, channels="BGR", use_column_width=True)
