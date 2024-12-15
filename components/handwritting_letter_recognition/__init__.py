import torch
import streamlit as st
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from services.handwriting_letter_recognition.model import MNISTModel

test_dataset = datasets.MNIST(
    "services/handwriting_letter_recognition",
    train=False,
    download=True,
    transform=transforms.ToTensor(),
)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=True)

device = "cpu"
model = MNISTModel().to(device)
model.load_state_dict(
    torch.load(
        "services/handwriting_letter_recognition/mnist_model.pth",
        weights_only=True,
        map_location=torch.device("cpu"),
    )
)
model.eval()


@st.cache_resource()
def test_phase():
    all_labels = []
    all_predicteds = []
    all_images = []

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
            all_images.extend(images.cpu().numpy())

    return all_labels, all_predicteds, all_images, correct / total
