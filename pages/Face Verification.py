import datetime
from PIL import Image
import streamlit as st
from google.cloud import firestore, storage
import pandas as pd

db = firestore.Client.from_service_account_json(
    "./face-recognize-7d75c-firebase-adminsdk-e2xa8-fe77725085.json"
)
bucket = storage.Client.from_service_account_json(
    "./face-recognize-7d75c-firebase-adminsdk-e2xa8-fe77725085.json"
).get_bucket("face-recognize-7d75c.appspot.com")

st.set_page_config(
    page_title="Face Verification",
    page_icon=Image.open("./public/images/logo.png"),
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Dữ liệu trong Firestore")

docs = db.collection("TheSV").stream()
data_table = {"id": [], "studentId": [], "path": [], "image": []}
for doc in docs:
    data_table["id"].append(doc.id)
    data_table["studentId"].append(doc.to_dict()["studentId"])
    data_table["path"].append(doc.to_dict()["path"])

    path = doc.to_dict()["path"].replace("gs://face-recognize-7d75c.appspot.com/", "")
    public_url = bucket.blob(path).generate_signed_url(
        datetime.timedelta(seconds=300), method="GET"
    )
    data_table["image"].append(f"<img src='{public_url}' width='150px'>")

st.header("1. Collection TheSV")
st.write(pd.DataFrame(data_table).to_html(escape=False), unsafe_allow_html=True)

docs_2 = db.collection("ChanDung").stream()
data_table_2 = {"id": [], "studentId": [], "path": [], "image": []}
for doc in docs_2:
    data_table_2["id"].append(doc.id)
    data_table_2["studentId"].append(doc.to_dict()["studentId"])
    data_table_2["path"].append(doc.to_dict()["path"])

    path = doc.to_dict()["path"].replace("gs://face-recognize-7d75c.appspot.com/", "")
    public_url = bucket.blob(path).generate_signed_url(
        datetime.timedelta(seconds=300), method="GET"
    )
    data_table_2["image"].append(f"<img src='{public_url}' width='150px'>")

st.header("2. Collection ChanDung")
st.write(pd.DataFrame(data_table_2).to_html(escape=False), unsafe_allow_html=True)
