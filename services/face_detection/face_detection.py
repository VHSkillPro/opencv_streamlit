import cv2

face_cascade = cv2.CascadeClassifier()
face_cascade.load("./services/face_detection/haarcascade_frontalface_default.xml")


def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)
    return faces
