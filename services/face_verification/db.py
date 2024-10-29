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
        """
        Get all documents from collection
        """

        print(datetime.datetime.now(), f">> INDEX {self.collection}")
        docs = self.db.collection(self.collection).stream()
        result = {}
        for doc in docs:
            result[doc.id] = doc.to_dict()
        return result

    def show(self, id: str):
        """
        Get a document by id

        Return:
        - Dict of document if found, else `None` if not found
        """

        print(datetime.datetime.now(), f">> SHOW {self.collection} {id}")
        return self.db.collection(self.collection).document(id).get().to_dict()

    def insert(self, docs: dict):
        """
        Insert a document to collection

        Input:
        - docs: Document to insert

        Return:
        - Reference to the new document
        """

        print(datetime.datetime.now(), f">> INSERT {self.collection}")
        new_doc_ref = self.db.collection(self.collection).document()
        new_doc_ref.set(docs)
        return new_doc_ref

    def update(self, id: str, docs: dict):
        """
        Update a document by id

        Input:
        - id: Document id to update
        - docs: Document to update

        Output:
        - `True` if success, else `False`
        """

        print(datetime.datetime.now(), f">> UPDATE {self.collection} {id}")
        try:
            self.db.collection(self.collection).document(id).update(docs)
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, id: str):
        """
        Delete a document by id

        Input:
        - id: Document id to delete

        Return:
        - `True` if success, else `False`
        """

        print(datetime.datetime.now(), f">> DELETE {self.collection} {id}")
        try:
            self.db.collection(self.collection).document(id).delete()
            return True
        except Exception as e:
            print(e)
            return False


class Storage(Database):
    def __init__(self) -> None:
        super().__init__()

    def get_url(self, path: str, expires_in: int = 300):
        """
        Get signed URL of a file in storage

        Input:
        - path: Path to file in storage
        - expires_in: Time to expire in seconds

        Return:
        - Signed URL of file
        """

        print(datetime.datetime.now(), ">> GET URL FROM STORAGE", path)
        return self.bucket.blob(path).generate_signed_url(
            datetime.timedelta(seconds=expires_in), method="GET"
        )

    def upload(self, path: str, file):
        """
        Upload a file to storage

        Input:
        - path: Path to upload file
        - file: File to upload
        """

        print(datetime.datetime.now(), ">> UPLOAD TO STORAGE", path)
        self.bucket.blob(path).upload_from_file(file)
