import os
import numpy as np

DATASET_DIR = "./services/image_search_engine/val2017"
image_names = os.listdir(os.path.join(DATASET_DIR, "images"))

vectors = []
for image_name in image_names:
    image_name_without_extension = os.path.splitext(image_name)[0]
    frequency_vector = np.load(
        os.path.join(DATASET_DIR, "vectors", f"{image_name_without_extension}.npy")
    )
    vectors.append(frequency_vector)
vectors = np.array(vectors)

print("Loaded vectors:", vectors.shape)
