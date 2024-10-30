import cv2, re
import numpy as np
from io import BytesIO
from PIL import Image, ImageOps
from services.face_verification.ultis import remove_vietnamese_accent
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

    def detect_single_face_multiscale(self, img: np.ndarray, scale_factor: float = 1.1):
        """
        Detect single face on image with multi-scale

        ### Arguments:
            img - Image to detect face
            scale_factor - Scale factor to resize image

        ### Returns:
            Detected single face
        """
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

    def find(self, student_id: str = "", student_name: str = ""):
        """
        Find students by student_id and student_name

        ### Arguments:
            student_id - Student id to find
            student_name - Student name to find

        ### Returns:
            List of filtered students
        """
        # Get all students
        students = self.repository.index()

        # Remove Vietnamese accent
        student_id = remove_vietnamese_accent(student_id)
        student_name = remove_vietnamese_accent(student_name)

        filtered_students = {}
        for key, data in students.items():
            is_match = True
            id = remove_vietnamese_accent(data["id"])
            name = remove_vietnamese_accent(data["name"])

            # Check if student id match
            if not re.search(student_id, id, re.IGNORECASE):
                is_match = False

            # Check if student name match
            if not re.search(student_name, name, re.IGNORECASE):
                is_match = False

            # Add to filtered students
            if is_match:
                filtered_students[key] = data

        return filtered_students

    def find_by_student_id(self, student_id: str):
        """
        Find student by student_id

        ### Arguments:
            student_id - Student id to find

        ### Returns:
            Student if found, `None` otherwise
        """
        collections = self.repository.db.collection("students")
        students = collections.where("id", "==", student_id).stream()

        result = {}
        for student in students:
            result[student.id] = student.to_dict()
            return result

        return None

    def insert(
        self, student_id: str, name: str, card: UploadedFile, selfie: UploadedFile
    ) -> str:
        """
        Insert new student to database

        ### Arguments:
            student_id - Student id
            name - Student name
            card - Student card image
            selfie - Student selfie image

        ### Returns:
            Message after insert student
        """

        # Check student exists
        student = self.find_by_student_id(student_id)
        if student is not None:
            return "Sinh viên đã tồn tại"

        # Convert uploaded file to image
        _card = Image.open(BytesIO(card.getbuffer()))
        card_img = ImageOps.exif_transpose(_card)
        card_img = cv2.cvtColor(np.array(card_img), cv2.COLOR_RGB2BGR)

        _selfie = Image.open(BytesIO(selfie.getbuffer()))
        selfie_img = ImageOps.exif_transpose(_selfie)
        selfie_img = cv2.cvtColor(np.array(selfie_img), cv2.COLOR_RGB2BGR)

        # Detect single face on card
        card_face, card_scale = self.detect_single_face_multiscale(card_img)
        if len(card_face) == 0:
            return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
        if len(card_face) > 1:
            return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

        # Detect single face on selfie
        selfie_face, selfie_scale = self.detect_single_face_multiscale(selfie_img)
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

        # Extract features
        card_feature = self.embedder.infer(resized_card, card_face[0][:-1])
        selfie_feature = self.embedder.infer(resized_selfie, selfie_face[0][:-1])

        # Check if card and selfie are the same person
        _, match = self.embedder.match_feature(card_feature, selfie_feature)
        if match == 0:
            return "Ảnh thẻ sinh viên và ảnh chân dung không cùng một người"

        # Save images to storage
        self.storage.upload(f"TheSV/{student_id}_card.jpg", card)
        self.storage.upload(f"ChanDung/{student_id}_selfie.jpg", selfie)

        # Insert student to database
        docs = {
            "id": student_id,
            "name": name,
            "card": f"TheSV/{student_id}_card.jpg",
            "selfie": f"ChanDung/{student_id}_selfie.jpg",
            "card_face_feature": card_feature[0].tolist(),
            "selfie_face_feature": selfie_feature[0].tolist(),
        }

        self.repository.insert(docs)
        return "Thêm sinh viên thành công"

    def update(
        self,
        student_id: str,
        name: str,
        card: UploadedFile | None,
        selfie: UploadedFile | None,
    ) -> str:
        """
        Update student by student_id

        ### Arguments:
            student_id - Student id to update
            name - Student name
            card - Student card image
            selfie - Student selfie image

        ### Returns:
            Message after update student
        """

        # Check student exists
        student = self.find_by_student_id(student_id)
        if student is None:
            return f"Sinh viên {student_id} không tồn tại"

        # Get student key and data
        key = list(student.keys())[0]
        student = list(student.values())[0]

        # Convert uploaded file to image and detect face in card image
        card_img, card_feature = None, None
        if card is not None:
            _card = Image.open(BytesIO(card.getbuffer()))
            card_img = ImageOps.exif_transpose(_card)
            card_img = cv2.cvtColor(np.array(card_img), cv2.COLOR_RGB2BGR)

            card_face, card_scale = self.detect_single_face_multiscale(card_img)
            if len(card_face) == 0:
                return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
            if len(card_face) > 1:
                return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

            resized_card = cv2.resize(
                card_img.copy(),
                (
                    int(card_img.shape[1] * card_scale),
                    int(card_img.shape[0] * card_scale),
                ),
            )

            card_feature = self.embedder.infer(resized_card, card_face[0][:-1])
            card_feature = np.array(card_feature)

        # Convert uploaded file to image and detect face in selfie image
        selfie_img, selfie_feature = None, None
        if selfie is not None:
            _selfie = Image.open(BytesIO(selfie.getbuffer()))
            selfie_img = ImageOps.exif_transpose(_selfie)
            selfie_img = cv2.cvtColor(np.array(selfie_img), cv2.COLOR_RGB2BGR)

            selfie_face, selfie_scale = self.detect_single_face_multiscale(selfie_img)
            if len(selfie_face) == 0:
                return "Không tìm thấy khuôn mặt trên ảnh thẻ sinh viên"
            if len(selfie_face) > 1:
                return "Tìm thấy nhiều khuôn mặt trên ảnh thẻ sinh viên"

            resized_selfie = cv2.resize(
                selfie_img.copy(),
                (
                    int(selfie_img.shape[1] * selfie_scale),
                    int(selfie_img.shape[0] * selfie_scale),
                ),
            )

            selfie_feature = self.embedder.infer(resized_selfie, selfie_face[0][:-1])
            selfie_feature = np.array(selfie_feature)

        # If update both card and selfie
        if (card is not None) and (selfie is not None):
            _, match = self.embedder.match_feature(card_feature, selfie_feature)
            if match == 0:
                return "Ảnh thẻ sinh viên và ảnh chân dung không cùng một người"

            self.storage.upload(f"TheSV/{student_id}_card.jpg", card)
            self.storage.upload(f"ChanDung/{student_id}_selfie.jpg", selfie)

            student["card"] = f"TheSV/{student_id}_card.jpg"
            student["selfie"] = f"ChanDung/{student_id}_selfie.jpg"
            student["card_face_feature"] = card_feature[0].tolist()
            student["selfie_face_feature"] = selfie_feature[0].tolist()

        # If update only card
        elif card is not None:
            _, match = self.embedder.match_feature(
                card_feature,
                np.array(
                    [student["selfie_face_feature"]],
                    dtype=np.dtype(card_feature[0][0]),
                ),
            )
            if match == 0:
                return "Ảnh thẻ sinh viên và ảnh chân dung không cùng một người"

            self.storage.upload(f"TheSV/{student_id}_card.jpg", card)
            student["card"] = f"TheSV/{student_id}_card.jpg"
            student["card_face_feature"] = card_feature[0].tolist()

        # If update only selfie
        elif selfie is not None:
            _, match = self.embedder.match_feature(
                np.array(
                    [student["card_face_feature"]],
                    dtype=np.dtype(selfie_feature[0][0]),
                ),
                selfie_feature,
            )
            if match == 0:
                return "Ảnh thẻ sinh viên và ảnh chân dung không cùng một người"

            self.storage.upload(f"ChanDung/{student_id}_selfie.jpg", selfie)
            student["selfie"] = f"ChanDung/{student_id}_selfie.jpg"
            student["selfie_face_feature"] = selfie_feature[0].tolist()

        student["name"] = name
        if self.repository.update(key, student):
            return "Cập nhật sinh viên thành công"
        return "Cập nhật sinh viên thất bại"

    def delete(self, student_id: str) -> str:
        """
        Delete student by student_id

        ### Arguments:
            student_id - Student id to delete

        ### Returns:
            Message after delete student
        """

        student = self.find_by_student_id(student_id)
        if student is None:
            return f"Sinh viên {student_id} không tồn tại"

        key = list(student.keys())[0]

        if self.repository.delete(key):
            return f"Xóa sinh viên {student_id} thành công"
        return f"Xóa sinh viên {student_id} thất bại"


class ClassService:
    def __init__(self) -> None:
        self.repository = Repository("classes")

    def find(self, class_id: str = "", class_name: str = ""):
        """
        Find classes by class_id and class_name

        Input:
        - class_id: str - Class id to find
        - class_name: str - Class name to find

        Returns:
        - List of filtered classes
        """

        # Get all classes
        classes = self.repository.index()

        # Remove Vietnamese accent
        class_id = remove_vietnamese_accent(class_id)
        class_name = remove_vietnamese_accent(class_name)

        filtered_classes = {}
        for key, data in classes.items():
            is_match = True
            id = remove_vietnamese_accent(data["id"])
            name = remove_vietnamese_accent(data["name"])

            # Check if class id match
            if not re.search(class_id, id, re.IGNORECASE):
                is_match = False

            # Check if class name match
            if not re.search(class_name, name, re.IGNORECASE):
                is_match = False

            # Add to filtered classes
            if is_match:
                filtered_classes[key] = data

        return filtered_classes

    def find_by_class_id(self, class_id: str):
        """
        Find class by class_id

        Input:
        - class_id: str - Class id to find

        Returns:
        - Class if found, `None` otherwise
        """

        collections = self.repository.db.collection("classes")
        classes = collections.where("id", "==", class_id).stream()

        result = {}
        for class_ in classes:
            result[class_.id] = class_.to_dict()
            return result

        return None

    def insert(self, class_id: str, name: str) -> str:
        """
        Insert new class to database

        Input:
        - class_id: str - Class id
        - name: str - Class name

        Returns:
        - Message after insert class
        """

        class_ = self.find_by_class_id(class_id)
        if class_ is not None:
            return f"Lớp {class_id} đã tồn tại"

        docs = {
            "id": class_id,
            "name": name,
        }

        self.repository.insert(docs)
        return f"Thêm lớp {class_id} thành công"

    def update(self, class_id: str, name: str) -> str:
        """
        Update class by class_id

        Input:
        - class_id: str - Class id
        - name: str - Class name

        Returns:
        - Message after update class
        """

        class_ = self.find_by_class_id(class_id)
        if class_ is None:
            return f"Lớp {class_id} không tồn tại"

        key = list(class_.keys())[0]
        class_ = list(class_.values())[0]

        class_["name"] = name
        if self.repository.update(key, class_):
            return f"Cập nhật lớp {class_id} thành công"
        return f"Cập nhật lớp {class_id} thất bại"

    def delete(self, class_id: str) -> str:
        """
        Delete class by class_id

        Input:
        - class_id: str - Class id to delete

        Returns:
        - Message after delete class
        """

        class_ = self.find_by_class_id(class_id)
        if class_ is None:
            return f"Lớp {class_id} không tồn tại"

        key = list(class_.keys())[0]

        if self.repository.delete(key):
            return f"Xóa lớp {class_id} thành công"


class StudentClassService:
    def __init__(self) -> None:
        self.repository = Repository("students_classes")
        self.classService = ClassService()

    def find(self, class_id: str = "", student_id: str = "", student_name: str = ""):
        """
        Find students by class_id

        Input:
        - class_id: str - Class id to find

        Returns:
        - List of filtered students in class, `None` if class not found
        """
        # Lấy danh sách student_id từ bảng students_classes theo class_id
        students_classes_ref = self.repository.db.collection("students_classes")
        query = students_classes_ref.where("class_id", "==", class_id)
        students_classes_docs = query.stream()

        # Lấy danh sách student_id từ kết quả truy vấn
        student_ids = [doc.to_dict()["student_id"] for doc in students_classes_docs]
        if len(student_ids) == 0:
            return {}

        # Lấy thông tin chi tiết của từng sinh viên từ bảng students
        student_ref = self.repository.db.collection("students")
        students_doc = student_ref.where("id", "in", student_ids).stream()

        students = {}
        for student in students_doc:
            key = student.id
            data = student.to_dict()

            is_match = True
            id = remove_vietnamese_accent(data["id"])
            name = remove_vietnamese_accent(data["name"])

            # Check if student id match
            if not re.search(student_id, id, re.IGNORECASE):
                is_match = False

            # Check if student name match
            if not re.search(student_name, name, re.IGNORECASE):
                is_match = False

            # Add to filtered students
            if is_match:
                students[key] = data

        return students
