import numpy as np
from scipy.spatial import distance


def analyze_dist(detections, safe_dist):
    unsafe = set()
    
    # construct distance matrix for each pair of people
    if len(detections) > 1:
        centroids = np.array([r[2] for r in detections])
        dist_mat = distance.cdist(centroids, centroids,metric="euclidean")

        for i in range(dist_mat.shape[0]):
            # ignore calculated pairs and start from i + 1
            for j in range(i + 1, dist_mat.shape[1]):
                if dist_mat[i, j] < safe_dist:
                    unsafe.add(i)
                    unsafe.add(j)
                
    return unsafe
    