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
        result = {}
        for student in students:
            result[student.id] = student.to_dict()
            return result
        return None

    def insert(self, id: str, name: str, card: UploadedFile) -> str:
        # Check student exists
        student = self.find_by_id(id)
        if student is not None:
            return "Sinh viên đã tồn tại"

        _card = Image.open(BytesIO(card.getbuffer()))
        card_img = ImageOps.exif_transpose(_card)
        card_img = cv2.cvtColor(np.array(card_img), cv2.COLOR_RGB2BGR)

        # Detect face on card
        card_face, card_scale = self.__detect_faces(card_img)
        if len(card_face) == 0:
            return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
        if len(card_face) > 1:
            return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

        # Resize images
        resized_card = cv2.resize(
            card_img.copy(),
            (int(card_img.shape[1] * card_scale), int(card_img.shape[0] * card_scale)),
        )

        # Save images to storage
        self.storage.upload(f"TheSV/{id}_card.jpg", card)

        # Extract features
        card_feature = self.embedder.infer(resized_card, card_face[0][:-1])

        docs = {
            "id": id,
            "name": name,
            "card": f"TheSV/{id}_card.jpg",
            "selfie": f"ChanDung/{id}_selfie.jpg",
            "card_face_feature": card_feature[0].tolist(),
        }

        self.repository.insert(docs)
        return "Thêm sinh viên thành công"

    def update(self, id, name, card):
        student = self.find_by_id(id)
        if student is None:
            return "Sinh viên không tồn tại"

        key = list(student.keys())[0]
        student = list(student.values())[0]

        if card is not None:
            _card = Image.open(BytesIO(card.getbuffer()))
            card_img = ImageOps.exif_transpose(_card)
            card_img = cv2.cvtColor(np.array(card_img), cv2.COLOR_RGB2BGR)

            # Detect face on card
            card_face, card_scale = self.__detect_faces(card_img)
            if len(card_face) == 0:
                return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
            if len(card_face) > 1:
                return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

            # Resize images
            resized_card = cv2.resize(
                card_img.copy(),
                (
                    int(card_img.shape[1] * card_scale),
                    int(card_img.shape[0] * card_scale),
                ),
            )

            # Save images to storage
            self.storage.upload(f"TheSV/{id}_card.jpg", card)

            # Extract features
            card_feature = self.embedder.infer(resized_card, card_face[0][:-1])

            student["card"] = f"TheSV/{id}_card.jpg"
            student["card_face_feature"] = card_feature[0].tolist()

        student["name"] = name
        if self.repository.update(key, student):
            return "Cập nhật sinh viên thành công"
        return "Cập nhật sinh viên thất bại"

    def delete(self, id):
        student = self.find_by_id(id)
        if student is None:
            return f"Sinh viên {id} không tồn tại"

        key = list(student.keys())[0]

        if self.repository.delete(key):
            return f"Xóa sinh viên {id} thành công"
        return f"Xóa sinh viên {id} thất bại"
