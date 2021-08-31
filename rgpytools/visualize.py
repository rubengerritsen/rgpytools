#!/usr/bin/env python3

from vpython import *
import numpy as np

def draw_molecule(atom_coordinates, atom_radius = 0.3, bond_cutoff = 1.7, atom_types = []):
        #convert to vpython type vectors
        vpython_atoms = []
        for tmp_atom in atom_coordinates:
            vpython_atoms.append(vector(tmp_atom[0],tmp_atom[1], tmp_atom[2]))
            
        for i, at in enumerate(vpython_atoms):
            atom = sphere()
            atom.pos = at
            atom.radius = atom_radius
            if len(atom_types) > 0:
                if atom_types[i] == "C":
                    atom.color = vector(0,0.58,0.69)
                elif atom_types[i] == "H":
                    atom.color = vector(0.98,0.98,0.98)
                    atom.radius = atom.radius * 0.7
                else:
                    atom.color = vector(0,0.58,0.69)
            else:
                atom.color = vector(0,0.58,0.69)
        
        # find bonds by distance
        dr = atom_coordinates - atom_coordinates[:, np.newaxis]
        dist = np.linalg.norm(dr, axis=2)
        drawBond = (dist < bond_cutoff)
        for pair in np.argwhere(drawBond==True):
            if pair[1] > pair[0]:
                curve(vpython_atoms[pair[0]], vpython_atoms[pair[1]],  radius=0.05)

def draw_unitcell(a,b,c):
    curve(vector(0,0,0), vector(a[0], a[1], a[2]),  radius=0.05, color = vector(0.99,0.,0.))
    curve(vector(0,0,0), vector(b[0], b[1], b[2]),  radius=0.05, color = vector(0.,1.,0))
    curve(vector(0,0,0), vector(c[0], c[1], c[2]),  radius=0.05, color = vector(0.,0,1.))

def start_canvas(center):
    scene = canvas(width=1200, height=800)
    scene.center = vector(center[0], center[1], center[2])
    scene.caption = " " 
    axes = [vector(1,0,0), vector(0,1,0), vector(0,0,1)]
    return (scene, axes)