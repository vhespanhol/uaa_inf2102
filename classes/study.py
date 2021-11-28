import pickle
import numpy as np
from pyDOE import lhs
import pandas as pd
from  .toolkit.tools import errorMessage

## Class Study
class Study:
    def __init__(self, stName,path, nsamples,experiments = None, parameters = None, cases = None,objFuncs = None):
        self.stName = stName # Study name
        self.path = path #Path folder
        self.nsamples = nsamples #number of experiments
        self.npar = 0 #number of parameters
        self.nof = 0 #number of objective functions
        self.experiments = experiments #table of experiments
        self.baseFirst = True #if delta, which case is the base case
        
        if parameters is None:
            self.parameters = []
        else:
            self.parameters = parameters

        if objFuncs is None:
            self.objFuncs = []
        else:
            self.objFuncs = objFuncs

        if cases is None:
            self.cases = []
            self.ncases = 0
        else:
            self.cases = cases
        
    
    # Add parameter to Study    
    def addPar(self,par):
        if par.pName not in [aux.pName for aux in self.parameters]:
            self.parameters.append(par)
            self.npar +=1
            print('Parameter "%s" sucessfully added.' % (par.pName))
        else:
            errorMessage(1)
    
    # Remove parameter from Study
    def remPar(self,parname):
        if parname not in [aux.pName for aux in self.parameters]:
            errorMessage(2)
        else:
            for aux in self.parameters:
                if aux.pName == parname:
                    self.parameters.remove(aux)
                    self.npar -=1
                    print('Parameter "%s" sucessfully removed.' % (parname))
                    
    # Add case to Study    
    def addCase(self,case):
        
        if case.cName not in [aux.cName for aux in self.cases]:
            if self.ncases > 1:
                errorMessage(3)
            else:
                self.cases.append(case)
                self.ncases +=1
                print('Case "%s" sucessfully added.' % (case.cName))
        else:
            errorMessage(1)
    
    # Remove case from Study
    def remCase(self,parname):
        if parname not in [aux.cName for aux in self.cases]:
            errorMessage(2)
        else:
            for aux in self.cases:
                if aux.cName == parname:
                    self.cases.remove(aux)
                    self.ncases -=1
                    print('Case "%s" sucessfully removed.' % (parname))


    # Add OF to Study    
    def addOF(self,of):
        if of.ofName not in [aux.ofName for aux in self.objFuncs]:
            self.objFuncs.append(of)
            self.nof +=1
            print('Objective Function "%s" sucessfully added.' % (of.ofName))
        else:
            errorMessage(1)
    
    # Remove OF from Study
    def remOF(self,ofname):
        if ofname not in [aux.ofName for aux in self.objFuncs]:
            errorMessage(2)
        else:
            for aux in self.objFuncs:
                if aux.ofName == ofname:
                    self.objFuncs.remove(aux)
                    self.nof -=1
                    print('Objective Function "%s" sucessfully removed.' % ofname)

    # Save Study                
    def save(self):
        with open(self.path + '\\' + self.stName + '\\study.cls', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    # Design of experiments (DOE)        
    def designExp(self):
        design = lhs(self.npar, samples=self.nsamples)
        for i in range(self.npar):
            design[:, i] = self.parameters[i].applyDist(design[:, i])
        self.experiments = design
    
    # Change base case
    def changeBase(self):
        self.baseFirst = not self.baseFirst
