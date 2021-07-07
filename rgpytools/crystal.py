
import numpy as np

def fromCos(A: float, B: float, C: float, cosAB: float, cosAC: float, cosBC: float) -> float:
  a_vec = 6.277 * np.array([1,0,0])
  b_vec = 7.663 * np.array([cosAB, np.sqrt(1- cosAB**2), 0 ])
  c_vec = 14.363 * np.array([cosAC, (cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2), np.sqrt(1- cosAC**2 - ((cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2))**2)])
  return np.stack([a_vec, b_vec, c_vec])