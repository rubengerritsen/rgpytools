
from rgpytools import mmHandler
import numpy as np

def test_MM():
  mat = np.array([[1,2],[3,4]])
  mmHandler.writeMM("tmp.mm", mat)
  assert np.sum(mat - mmHandler.readMM("tmp.mm")) < 1e-8
