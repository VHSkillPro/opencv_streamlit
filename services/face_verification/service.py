# import cv2 as cv
# import numpy as np


# def visualize(
#     img1, faces1, img2, faces2, matches, scores, target_size=[512, 512]
# ):  # target_size: (h, w)
#     out1 = img1.copy()
#     out2 = img2.copy()
#     matched_box_color = (0, 255, 0)  # BGR
#     mismatched_box_color = (0, 0, 255)  # BGR

#     # Resize to 256x256 with the same aspect ratio
#     padded_out1 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
#     h1, w1, _ = out1.shape
#     ratio1 = min(target_size[0] / out1.shape[0], target_size[1] / out1.shape[1])
#     new_h1 = int(h1 * ratio1)
#     new_w1 = int(w1 * ratio1)
#     resized_out1 = cv.resize(
#         out1, (new_w1, new_h1), interpolation=cv.INTER_LINEAR
#     ).astype(np.float32)
#     top = max(0, target_size[0] - new_h1) // 2
#     bottom = top + new_h1
#     left = max(0, target_size[1] - new_w1) // 2
#     right = left + new_w1
#     padded_out1[top:bottom, left:right] = resized_out1

#     # Draw bbox
#     bbox1 = faces1[0][:4] * ratio1
#     x, y, w, h = bbox1.astype(np.int32)
#     cv.rectangle(
#         padded_out1,
#         (x + left, y + top),
#         (x + left + w, y + top + h),
#         matched_box_color,
#         2,
#     )

#     # Resize to 256x256 with the same aspect ratio
#     padded_out2 = np.zeros((target_size[0], target_size[1], 3)).astype(np.uint8)
#     h2, w2, _ = out2.shape
#     ratio2 = min(target_size[0] / out2.shape[0], target_size[1] / out2.shape[1])
#     new_h2 = int(h2 * ratio2)
#     new_w2 = int(w2 * ratio2)
#     resized_out2 = cv.resize(
#         out2, (new_w2, new_h2), interpolation=cv.INTER_LINEAR
#     ).astype(np.float32)
#     top = max(0, target_size[0] - new_h2) // 2
#     bottom = top + new_h2
#     left = max(0, target_size[1] - new_w2) // 2
#     right = left + new_w2
#     padded_out2[top:bottom, left:right] = resized_out2

#     # Draw bbox
#     assert faces2.shape[0] == len(matches), "number of faces2 needs to match matches"
#     assert len(matches) == len(
#         scores
#     ), "number of matches needs to match number of scores"
#     for index, match in enumerate(matches):
#         bbox2 = faces2[index][:4] * ratio2
#         x, y, w, h = bbox2.astype(np.int32)
#         box_color = matched_box_color if match else mismatched_box_color
#         cv.rectangle(
#             padded_out2, (x + left, y + top), (x + left + w, y + top + h), box_color, 2
#         )

#         score = scores[index]
#         text_color = matched_box_color if match else mismatched_box_color
#         cv.putText(
#             padded_out2,
#             "{:.2f}".format(score),
#             (x + left, y + top - 5),
#             cv.FONT_HERSHEY_DUPLEX,
#             0.4,
#             text_color,
#         )

#     return (padded_out1, padded_out2)

import cv2
import numpy as np
from io import BytesIO
from PIL import Image, ImageOps
from services.face_verification.yunet import YuNet
from services.face_verification.sface import SFace
from services.face_verification.db import Repository, Storage
from streamlit.runtime.uploaded_file_manager import UploadedFile


class StudentService:
    def __init__(self) -> None:
        self.repository = Repository("students")
        self.storage = Storage()
        self.detector = YuNet(
            "./services/face_verification/models/face_detection_yunet_2023mar.onnx",
            confThreshold=0.85,
        )
        self.embedder = SFace(
            "./services/face_verification/models/face_recognition_sface_2021dec.onnx"
        )

    def __detect_faces(self, img: np.ndarray, scale_factor: float = 1.1):
        org_h, org_w = img.shape[:2]

        scale = 1.0
        while scale * min(org_w, org_h) > 50:
            resized = cv2.resize(img.copy(), (int(org_w * scale), int(org_h * scale)))
            new_h, new_w = resized.shape[:2]

            self.detector.setInputSize((new_w, new_h))
            faces = self.detector.infer(resized)

            if len(faces) == 1:
                return (faces, scale)
            if len(faces) > 1:
                return ([], 1.0)

            scale /= scale_factor

        return ([], 1.0)

    def find(self, filter: object):
        students = self.repository.index()

        filtered_students = {}
        for key, data in students.items():
            is_match_id = (filter["id"] == "") or (
                filter["id"].lower() in data["id"].lower()
            )
            is_match_name = (filter["name"] == "") or (
                filter["name"].lower() in data["name"].lower()
            )
            if is_match_id and is_match_name:
                filtered_students[key] = data

        return filtered_students

    def find_by_id(self, id: str):
        students = (
            self.repository.db.collection("students").where("id", "==", id).stream()
        )
        for student in students:
            return student.to_dict()
        return None

    def insert(
        self, id: str, name: str, card: UploadedFile, selfie: UploadedFile
    ) -> str:
        # Check student exists
        student = self.find_by_id(id)
        if student is not None:
            return "Sinh viên đã tồn tại"

        _card = Image.open(BytesIO(card.getbuffer()))
        card_img = ImageOps.exif_transpose(_card)
        card_img = cv2.cvtColor(np.array(card_img), cv2.COLOR_RGB2BGR)

        _selfie = Image.open(BytesIO(selfie.getbuffer()))
        selfie_img = ImageOps.exif_transpose(_selfie)
        selfie_img = cv2.cvtColor(np.array(selfie_img), cv2.COLOR_RGB2BGR)

        # Detect face on card
        card_face, card_scale = self.__detect_faces(card_img)
        if len(card_face) == 0:
            return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
        if len(card_face) > 1:
            return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

        # Detect face on selfie
        selfie_face, selfie_scale = self.__detect_faces(selfie_img)
        if len(selfie_face) == 0:
            return "Không tìm thấy khuôn mặt trên ảnh chân dung"
        if len(selfie_face) > 1:
            return "Tìm thấy nhiều khuôn mặt trên ảnh chân dung"

        # Resize images
        resized_card = cv2.resize(
            card_img.copy(),
            (int(card_img.shape[1] * card_scale), int(card_img.shape[0] * card_scale)),
        )
        resized_selfie = cv2.resize(
            selfie_img.copy(),
            (
                int(selfie_img.shape[1] * selfie_scale),
                int(selfie_img.shape[0] * selfie_scale),
            ),
        )

        # Save images to storage
        self.storage.upload(f"TheSV/{id}_card.jpg", card)
        self.storage.upload(f"ChanDung/{id}_selfie.jpg", selfie)

        # Extract features
        card_feature = self.embedder.infer(resized_card, card_face[0][:-1])
        selfie_feature = self.embedder.infer(resized_selfie, selfie_face[0][:-1])

        docs = {
            "id": id,
            "name": name,
            "card": f"TheSV/{id}_card.jpg",
            "selfie": f"ChanDung/{id}_selfie.jpg",
            "card_face_feature": card_feature[0].tolist(),
            "selfie_face_feature": selfie_feature[0].tolist(),
        }

        self.repository.insert(docs)
        return "Thêm sinh viên thành công"
