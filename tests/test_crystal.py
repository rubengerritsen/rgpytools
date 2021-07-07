
from rgpytools import crystal
import numpy as np


def test_fromCos():
  A = 6.277 
  B = 7.663
  C = 14.363
  cosAB = 0.2267702
  cosAC = 0.031172476
  cosBC = 0.09886819

  uc_ref = np.array([[6.2770000000,       0.0000000000,       0.0000000000],
        [1.7377400426,       7.4633657651,       0.0000000000],
        [0.4477302728,       1.3537802157,      14.2920462401]])

  res = crystal.fromCos(A, B, C, cosAB, cosAC, cosBC) - uc_ref
  assert np.sum(res) < 1e-8

