import streamlit as st
import keras
import json

with open("services\handwriting_letter_recognition\history.json", "r") as fi:
    history = json.load(fi)
history["epoch"] = list(range(1, 21))


@st.fragment()
def display_result():
    st.header("3. Kết quả huấn luyện")

    st.line_chart(
        history,
        x="epoch",
        x_label="Epoch",
        y_label="Loss|Accuracy",
        use_container_width=True,
    )
