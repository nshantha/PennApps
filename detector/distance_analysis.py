import numpy as np
from scipy.spatial import distance
import cv2


def analyze_dist(detections, prespective_transform, xdist_in_pixels, ydist_in_pixels, safe_dist = 6):
    unsafe = set()
    
    # construct distance matrix for each pair of people
    if len(detections) > 1:
        # centroids = np.array([r[2] for r in detections])
        centroids = [r[2] for r in detections]
        # print(centroids)


        centroids_trans = []
        for centroid in centroids:
            centroid = np.array([[[int(centroid[0]),int(centroid[1])]]] , dtype="float32")
            # print(centroid)
            bd_pnt = cv2.perspectiveTransform(centroid, prespective_transform)[0][0]
            pnt = [int(bd_pnt[0]), int(bd_pnt[1])]
            # print(pnt)
            centroids_trans.append(pnt)

        centroids = np.array(centroids_trans)
        # print(centroids)
        centroids[:, 0] = centroids[:, 0] * 6 / xdist_in_pixels
        centroids[:, 1] = centroids[:, 1] * 6 / ydist_in_pixels
        # print(centroids)
            

        dist_mat = distance.cdist(centroids, centroids,metric="euclidean")

        for i in range(dist_mat.shape[0]):
            # ignore calculated pairs and start from i + 1
            for j in range(i + 1, dist_mat.shape[1]):
                if dist_mat[i, j] < safe_dist:
                    unsafe.add(i)
                    unsafe.add(j)
                
    return unsafe
    