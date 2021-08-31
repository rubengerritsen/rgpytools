#!/usr/bin/env python3

import numpy as np
from scipy.spatial.transform import Rotation

def rotateCoord(coordinates, rotationVector):
    r = Rotation.from_rotvec(rotationVector)
    return (r.as_matrix() @ coordinates.T).T

def align_vectors(a, b):
    b = b / np.linalg.norm(b) # normalize a
    a = a / np.linalg.norm(a) # normalize b
    v = np.cross(a, b)
    # s = np.linalg.norm(v)
    c = np.dot(a, b)
    v1, v2, v3 = v
    h = 1 / (1 + c)
    Vmat = np.array([[0, -v3, v2],
                  [v3, 0, -v1],
                  [-v2, v1, 0]])

    R = np.eye(3, dtype=np.float64) + Vmat + (Vmat.dot(Vmat) * h)
    return R