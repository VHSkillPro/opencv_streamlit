import json
import datetime
import numpy as np
import streamlit as st
from google.cloud import firestore, storage
from google.cloud.firestore import FieldFilter
from streamlit.runtime.uploaded_file_manager import UploadedFile


class Service:
    def __init__(self) -> None:
        key_dict = json.loads(st.secrets["textkey"])
        self.db = firestore.Client.from_service_account_info(key_dict)
        self.bucket = storage.Client.from_service_account_info(key_dict).get_bucket(
            "face-recognize-7d75c.appspot.com"
        )

    def parse_data(self, docs):
        result = {}
        for doc in docs:
            result[doc.id] = doc.to_dict()
        return result

    def get_all(self, collection):
        print(
            datetime.datetime.now(), ">> Get all documents from collection", collection
        )
        docs = self.db.collection(collection).stream()
        return self.parse_data(docs)

    def add(self, collection, data):
        print(datetime.datetime.now(), ">> Add new document to collection", collection)
        new_doc_ref = self.db.collection(collection).document()
        new_doc_ref.set(data)
        return True

    def delete(self, collection, id):
        print(datetime.datetime.now(), ">> Delete document from collection", collection)
        self.db.collection(collection).document(id).delete()
        return True

    def get_url_from_storage(self, path, expires_in=300):
        print(datetime.datetime.now(), ">> Get public url from storage", path)
        public_url = self.bucket.blob(path).generate_signed_url(
            datetime.timedelta(seconds=expires_in), method="GET"
        )
        return public_url


class StudentService(Service):
    def __init__(self) -> None:
        super().__init__()

    def get_all(self):
        result = super().get_all("students")
        return result

    def find_like(self, id: str):
        print(datetime.datetime.now(), ">> Find student like id", id)
        datas = self.get_all()

        result = {}
        for key, data in datas.items():
            if id.lower() in data["id"].lower():
                result[key] = data

        return result

    def find_by(self, id: str):
        print(datetime.datetime.now(), ">> Find student by id", id)
        docs = (
            self.db.collection("students")
            .where(filter=FieldFilter("id", "==", id))
            .stream()
        )
        return self.parse_data(docs)

    def add(self, id: str, card: UploadedFile, selfie: UploadedFile) -> bool:
        if id.strip() == "" or card is None or selfie is None:
            return

        if len(self.find_by(id)) > 0:
            return False

        print(datetime.datetime.now(), ">> Add new student")

        # Upload images to storage
        card_path = f"TheSV/{card.name}"
        self.bucket.blob(card_path).upload_from_file(card)

        selfie_path = f"ChanDung/{selfie.name}"
        self.bucket.blob(selfie_path).upload_from_file(selfie)

        data = {
            "id": id,
            "card": card_path,
            "selfie": selfie_path,
        }

        return super().add("students", data)

    def delete(self, id: str) -> bool:
        if id.strip() == "":
            return

        students = self.find_by(id)
        if len(students) == 0:
            return False

        print(datetime.datetime.now(), ">> Delete student")

        student = list(students.values())[0]
        return super().delete("students", list(students.keys())[0])
