
import numpy as np
import h5py
import argparse

def helpMessage():
  return("""
  Wrapper for VOTCA-XTP orbitals.
  --------------------------------
  Standalone mode: Converts a VOTCA-XTP checkpoint file (.hdf5) to an orbitals (.orb) file.
  As Module: Wraps either a .orb file or the qm part of a checkpoint file for easy access.
  """)

def moduleHelp():
  return(helpMessage())

class Orbitals:
    
    def __init__(self, hdf5File, h5pyGroup):
        """ Creates an orbitals object from an HDF5 file and an h5py group.
        
        Input: the hdf5 file and the h5py group pointing to the QM data (orbitals).
        """
        self.orb = h5pyGroup
        self.hdf5File = hdf5File
        self.hrt2ev = 27.211396132
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.hdf5File.close()
    
    @classmethod
    def fromOrb(cls, fileName: str):
        """ Reads a .orb file and transforms its contents to NumPy objects.
        
        Input: a basic .orb file (no checkpoint files)
        """
        if (fileName[-4:] != ".orb"):
            raise NameError(f"fromOrb only reads .orb files")
        else:
            hdf5File = h5py.File(fileName, 'r+')
            orb = hdf5File['QMdata']
        return cls(hdf5File, orb)
         
    @classmethod
    def fromQMMMCpt(cls, fileName, regionName = "region_0"):
        """ Takes a QMMM checkpoint file and turns it into an orbitals object.
        
        Input: A QMMM checkpoint file and a regionName pointing to a QM region
        in the HDF5 file.
        Returns an orbitals object
        """
        hdf5File = h5py.File(fileName, 'r+')
        if regionName + "/orbitals" in hdf5File:
            orb = hdf5File[regionName + "/orbitals"]
        else:
            raise NameError(f"{regionName} in QMMMCpt file {fileName} is not a QM region.")
        return cls(hdf5File, orb)
    
    def writeToOrbFile(self, fileName = "h5pyOutput.orb"):
        with h5py.File(fileName, "w") as out:
            out.copy(self.orb, 'QMdata')
          
    def readGroupOfArraysHDF5(self, topGroup, groupToRead):
        """ Read groups of arrays from HDF5 files based on the VOTCA output.
        
        VOTCA prints vectors of arrays/vectors as a group of datasets to the HDF5
        file. Every dataset is labeled with "ind###" where ### stands for the 
        index in the original vector. A standard HDF5 import via h5py can't 
        understand this ordering, hence we need to sort the imported elements.
        
        Input: 
              topGroup: an h5py group object containing only datasets 
              groupToRead: name of group to read as a String 
        Output:
              np-array containing every dataset as a row.
        """
        groupedData = []
        permutation = []
        for ind in topGroup[groupToRead].keys():
              permutation.append(int(ind[3:])) # 3: skips over the 'ind' bit
              groupedData.append(self.orb[groupToRead][ind][:].transpose()[0])
        groupedData = np.asarray(groupedData)
        return(groupedData[np.argsort(permutation)])
    
    def getTransitionDipoles(self):
        return self.readGroupOfArraysHDF5(self.orb, "transition_dipoles")

    def getOscillatorStrenghts(self):
      """ Returns oscillator strengths, scaled from Hartree to eV. """
      return 2.0/3.0 * np.linalg.norm(self.getTransitionDipoles(), axis = 1)**2 * self.getSingletEnergies() / self.hrt2ev

    def getTotalQMEnergy(self):
        return self.orb.attrs['qm_energy'][0] * self.hrt2ev
    
    def getEnergies(self):
        """ In eV """
        return self.orb['mos']['eigenvalues'][()].transpose()[0]  * self.hrt2ev
    
    def getMOs(self):
        return self.orb['mos']['eigenvectors'][()]
    
    def getAlphaMOs(self):
        return self.getMOs()
    
    def getBetaMOs(self):
        return self.orb['mos']['eigenvectors2'][()]
    
    def getSingletEnergies(self):
        """ Returns singlet energy in eV """ 
        return  self.orb['BSE_singlet']['eigenvalues'][()].transpose()[0] * self.hrt2ev
    
    def getSingletMOsA(self):
        return self.orb['BSE_singlet']['eigenvectors'][()]
    
    def getSingletMOsB(self):
        return self.orb['BSE_singlet']['eigenvectors'][()]
        
    def getTripletEnergies(self):
        """ In eV """
        return  self.orb['BSE_triplet']['eigenvalues'][()].transpose()[0] * self.hrt2ev
    
    def getTripletMOsA(self):
        return self.orb['BSE_triplet']['eigenvectors'][()]
    
    def getTripletMOsB(self):
        return self.orb['BSE_triplet']['eigenvectors'][()]
    
    def getQPPertEnergies(self):
        """ In eV """
        return  self.orb['QPpert_energies'][()].transpose()[0]
    
    def getQPDiagEigenVal(self):
        return  self.orb['QPdiag']['eigenvalues'][()].transpose()[0] * self.hrt2ev
    
    def getQPDiag(self):
        return self.orb['QPdiag']['eigenvectors'][()]
    
    def getQPDiag2(self):
        return self.orb['QPdiag']['eigenvectors'][()]
    
    def rpaInputEnergies(self):
        """ in eV """
        return self.orb['RPA_inputenergies'][()]  * self.hrt2ev
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter, 
    description=helpMessage())
    parser.add_argument('checkpointfile', metavar='file', type=str,
                    help='File name of the Checkpoint file to convert.')
    parser.add_argument('-r', metavar='region', type=str,
                    help='Name of QM region in checkpoint file.')
    parser.add_argument('--moduleHelp', 
                    help="displays help of the orbitals wrapper module.", 
                    action="store_true")

    args = parser.parse_args()

    if args.moduleHelp:
        print(moduleHelp())

    if len(userOptions) == 1:
        print("This tool can only convert QMMM checkpoint files to .orb files.")
        print("Please provide the name of the QMMM checkpoint file as an option.")
        print("For a more detailed help message use the option help.")
    else:
        if (len(userOptions) == 2): 
          if (len(userOptions[1]) > 5 and userOptions[-5:] == '.hdf5'):
              with Orbitals.fromQMMMCpt(userOptions[1]) as checkpointFile:
                  checkpointFile.writeToOrbFile()

    with Orbitals.fromQMMMCpt("checkpoint_iter_1.hdf5", "region_0") as orb:
        print(orb.getEnergies())
