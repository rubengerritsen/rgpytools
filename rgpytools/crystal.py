
import numpy as np

def ucVecFromCos(A: float, B: float, C: float, cosAB: float, cosAC: float, cosBC: float) -> float:
  """ Returns unit cell matrix of triclinic box. """
  a_vec = A * np.array([1,0,0])
  b_vec = B * np.array([cosAB, np.sqrt(1- cosAB**2), 0 ])
  c_vec = C * np.array([cosAC, (cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2), np.sqrt(1- cosAC**2 - ((cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2))**2)])
  return (a_vec, b_vec, c_vec)

def ucVecFromAngles(A: float, B: float, C: float, alpha: float, beta: float, gamma: float) -> float:
  """ Returns unit cell matrix of triclinic box. """
  cosAB = np.cos(np.deg2rad(gamma))
  cosAC = np.cos(np.deg2rad(beta))
  cosBC = np.cos(np.deg2rad(alpha))
  a_vec = A * np.array([1,0,0])
  b_vec = B * np.array([cosAB, np.sqrt(1- cosAB**2), 0 ])
  c_vec = C * np.array([cosAC, (cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2), np.sqrt(1- cosAC**2 - ((cosBC- cosAC*cosAB)/np.sqrt(1-cosAB**2))**2)])
  return (a_vec, b_vec, c_vec)