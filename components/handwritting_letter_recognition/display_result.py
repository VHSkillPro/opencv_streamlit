import json
import seaborn as sns
import streamlit as st
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix
from components.handwritting_letter_recognition import test_phase

with open("services/handwriting_letter_recognition/history.json", "r") as fi:
    history = json.load(fi)
history["epoch"] = list(range(1, 21))


@st.fragment()
def display_result():
    st.header("3. Kết quả")

    st.write("- Kết quả huấn luyện:")
    st.line_chart(
        history,
        x="epoch",
        x_label="Epoch",
        y_label="Loss | Accuracy",
        use_container_width=True,
    )

    labels, predicteds, __, accuracy = test_phase()
    st.write(f"- Đánh giá trên test set với **accuracy** = ${accuracy:.4f}$.")
    st.write("- Kết quả của ma trận nhầm lẫn:")

    cm = confusion_matrix(labels, predicteds)
    fig = plt.figure(figsize=(10, 8))
    ax = fig.subplots(1, 1)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        ax=ax,
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    st.columns([1, 3, 1])[1].pyplot(fig)
