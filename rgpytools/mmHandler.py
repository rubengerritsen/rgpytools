#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 16:12:57 2020

@author: ruben
"""

import numpy as np
def readMM(filename) -> np.array:
    with open(filename, "r") as input:
        line = input.readline()
        line = input.readline().split()
        rows = int(line[0])
        cols = int(line[1])
        numbers = []
        for line in input:
            numbers.append(float(line))
        npMatrix = np.array(numbers)
        npMatrix = npMatrix.reshape((rows,cols), order='F')
        return npMatrix

def writeMM(filename, mat):
    with open(filename, "w") as output:
        output.write("%%MatrixMarket matrix array real general\n")
        output.write(f"{mat.shape[0]} {mat.shape[1]}\n")
        mat = mat.reshape(mat.shape[0]*mat.shape[1],order='F')
        for number in mat:
            output.write(str(number)+ "\n")