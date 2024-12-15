import json
from matplotlib import pyplot as plt
import torch
import streamlit as st
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from services.handwriting_letter_recognition.model import MNISTModel
from sklearn.metrics import confusion_matrix
import seaborn as sns

test_dataset = datasets.MNIST(
    "services/handwriting_letter_recognition",
    train=False,
    download=True,
    transform=transforms.ToTensor(),
)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=True)

with open("services/handwriting_letter_recognition/history.json", "r") as fi:
    history = json.load(fi)
history["epoch"] = list(range(1, 21))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MNISTModel().to(device)
model.load_state_dict(
    torch.load(
        "services/handwriting_letter_recognition/mnist_model.pth", weights_only=True
    )
)
model.eval()


@st.cache_resource()
def test_phase():
    all_labels = []
    all_predicteds = []

    with torch.no_grad():
        correct = 0
        total = len(test_dataset)
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            probabilities = torch.softmax(outputs, dim=1)
            predicted = torch.argmax(probabilities, dim=1)
            correct += (predicted == labels).sum().item()

            all_labels.extend(labels.cpu().numpy())
            all_predicteds.extend(predicted.cpu().numpy())

    return all_labels, all_predicteds, correct / total


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

    labels, predicteds, accuracy = test_phase()
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
