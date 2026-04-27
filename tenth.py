# kmeans_numpy_reduced.py
import numpy as np
from sklearn.datasets import make_blobs

def initialize_centroids(X, k):
    return X[np.random.choice(len(X), k, replace=False)]

def assign_clusters(X, centroids):
    distances = np.sqrt(((X - centroids[:, np.newaxis])**2).sum(axis=2))
    return np.argmin(distances, axis=0)

def update_centroids(X, labels, k):
    return np.array([X[labels == i].mean(axis=0) for i in range(k)])

def kmeans_numpy(X, k, max_iters=100):
    centroids = initialize_centroids(X, k)
    for _ in range(max_iters):
        labels = assign_clusters(X, centroids)
        new_centroids = update_centroids(X, labels, k)
        if np.allclose(centroids, new_centroids):
            break
        centroids = new_centroids
    return labels, centroids

# Example
X, y_true = make_blobs(n_samples=200, centers=3, random_state=42)
labels, centers = kmeans_numpy(X, 3)
print("Final Centroids:\n", centers)
