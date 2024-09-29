import cv2
import numpy as np
import xml.etree.ElementTree as ET
from sklearn.neighbors import KNeighborsClassifier


class Extractor:
    def __init__(self, cascade_file):
        self.haar_features = []
        cascade = ET.parse(cascade_file)
        features = cascade.getroot().findall(".//features/_/rects")
        for feature in features:
            haar_feature = []
            rects = feature.findall("_")
            for rect in rects:
                x, y, w, h, wt = map(int, map(float, rect.text.strip().split()))
                haar_feature.append((x, y, w, h, wt))
            self.haar_features.append(haar_feature)

    def extract_feature_image(self, img):
        """Extract the haar feature for the current image"""
        image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, (24, 24))
        ii = cv2.integral(image)
        features = []
        for haar_feature in self.haar_features:
            value = 0
            for rect in haar_feature:
                x, y, w, h, wt = rect
                value += wt * (
                    ii[y + h][x + w] + ii[y][x] - ii[y][x + w] - ii[y + h][x]
                )
            features.append(value)
        return features


# face_cascade = cv2.CascadeClassifier()
# face_cascade.load("./services/face_detection/haarcascade_frontalface_default.xml")
extractor = Extractor("./services/face_detection/cascade.xml")
model = KNeighborsClassifier(n_neighbors=50)
X = np.load("./services/face_detection/X.npy")
y = np.load("./services/face_detection/y.npy")
model.fit(X, y)


def detect_faces(image):
    faces = []
    for k in np.array([4]):
        sz = min(24 * k, image.shape[0], image.shape[1])
        for x in range(0, image.shape[1] - sz, 5):
            for _y in range(0, image.shape[0] - sz, 5):
                img = image[_y : _y + sz, x : x + sz]
                features = extractor.extract_feature_image(img)
                if model.predict([features])[0] == 1:
                    faces.append((x, _y, sz, sz))

    # faces = face_cascade.detectMultiScale(gray)
    return faces
