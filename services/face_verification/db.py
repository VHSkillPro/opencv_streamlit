import json
import datetime
import streamlit as st
from google.cloud import firestore, storage


class Database:
    def __init__(self) -> None:
        key_dict = json.loads(st.secrets["textkey"])
        self.db = firestore.Client.from_service_account_info(key_dict)
        self.bucket = storage.Client.from_service_account_info(key_dict).get_bucket(
            "face-recognize-7d75c.appspot.com"
        )


class Repository(Database):
    def __init__(self, collection: str) -> None:
        super().__init__()
        self.collection = collection

    def index(self):
        print(datetime.datetime.now(), f">> INDEX {self.collection} >>")
        docs = self.db.collection(self.collection).stream()
        result = {}
        for doc in docs:
            result[doc.id] = doc.to_dict()
        return result

    def show(self, id):
        print(datetime.datetime.now(), f">> SHOW {self.collection} {id} >>")
        return self.db.collection(self.collection).document(id).get().to_dict()

    def insert(self, docs):
        print(datetime.datetime.now(), f">> INSERT {self.collection} >>")
        new_doc_ref = self.db.collection(self.collection).document()
        new_doc_ref.set(docs)
        return new_doc_ref

    def update(self, id, docs):
        print(datetime.datetime.now(), f">> UPDATE {self.collection} {id} >>", docs)
        try:
            return self.db.collection(self.collection).document(id).update(docs)
        except Exception as e:
            return False

    def delete(self, id):
        print(datetime.datetime.now(), f">> DELETE {self.collection} {id}")
        self.db.collection(self.collection).document(id).delete()


class Storage(Database):
    def __init__(self) -> None:
        super().__init__()

    def get_url(self, path, expires_in=300):
        print(datetime.datetime.now(), ">> GET URL FROM STORAGE", path)
        return self.bucket.blob(path).generate_signed_url(
            datetime.timedelta(seconds=expires_in), method="GET"
        )

    def upload(self, path, file):
        print(datetime.datetime.now(), ">> UPLOAD TO STORAGE", path)
        self.bucket.blob(path).upload_from_file(file)
