#!/usr/bin/env python3

import numpy as np

def readFile(filename: str):
  xyz_file = np.genfromtxt(fname=filename, skip_header=2, dtype='unicode')
  symbols = xyz_file[:,0]
  coordinates = (xyz_file[:,1:])
  coordinates = coordinates.astype(float)
  return (symbols, coordinates)