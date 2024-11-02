import numpy as np

# from faiss import Kmeans
from scipy.cluster.vq import vq
from tqdm import tqdm


# class BoVW:
#     def __init__(self, k_visual_word=1024, dimension=256) -> None:
#         self.k_visual_word = k_visual_word
#         self.dimension = dimension
#         self.kmeans = Kmeans(d=dimension, k=k_visual_word, verbose=True, gpu=True)

#     def fit(self, X: np.ndarray) -> None:
#         assert (
#             len(X.shape) == 2 and X.shape[1] == self.dimension
#         ), f"X should be 2D array with shape (n_samples, {self.dimension})"
#         self.kmeans.train(X)

#     def get_codebook(self) -> np.ndarray:
#         return self.kmeans.centroids


class VectorQuantization:
    def __init__(self, codebook: np.ndarray, idf: np.ndarray = None) -> None:
        if idf is not None:
            assert len(idf.shape) == 1, "idf should be 1D array"
            assert idf.shape[0] == codebook.shape[0], "Dimension mismatch"
        self.codebook = codebook
        self.idf = idf

    def fit(self, X: list[np.ndarray]) -> None:
        """
        Compute frequency vector for each image in X

        :param X: list of 2D array with shape (n_samples, dimension)
        :return: frequency_vectors: 2D array with shape (n_samples, k_visual_word)
        """

        dimension = X[0].shape[1]
        for i in range(len(X)):
            assert (
                len(X[i].shape) == 2 and X[i].shape[1] == dimension
            ), f"X[{i}] should be 2D array with shape (n_samples, {dimension})"

        # Compute visual words
        visual_words = []
        for x in tqdm(X, desc="Computing visual words"):
            visual_word, _ = vq(x, self.codebook)
            visual_words.append(visual_word)

        # Compute frequency vector
        frequency_vectors = []
        for img_visual_words in tqdm(visual_words, "Computing frequency vectors"):
            img_frequency_vector = np.zeros(self.codebook.shape[0])
            for word in img_visual_words:
                img_frequency_vector[word] += 1
            frequency_vectors.append(img_frequency_vector)
        frequency_vectors = np.stack(frequency_vectors)

        # Using tf-idf to normalize frequency vector
        N = len(X)
        df = np.sum(frequency_vectors > 0, axis=0)
        self.idf = np.log(N / df)

        self.frequency_vectors = frequency_vectors * self.idf
        return self.frequency_vectors

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Compute frequency vector for descriptors X of an image

        :param X: descriptors of an image with shape (n_samples, dimension)
        :return: frequency_vector: 1D array with shape (k_visual_word)
        """

        assert self.idf is not None, "You should fit the model first"
        assert len(X.shape) == 2, "X should be 2D array"
        assert X.shape[1] == self.codebook.shape[1], "Dimension mismatch"

        # Compute frequency vector
        visual_words, _ = vq(X, self.codebook)
        frequency_vector = np.zeros(self.codebook.shape[0])
        for word in visual_words:
            frequency_vector[word] += 1

        # Using tf-idf to normalize frequency vector
        frequency_vector *= self.idf
        return frequency_vector
