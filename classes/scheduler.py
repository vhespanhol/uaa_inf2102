#from __future__ import with_statement
import pickle
import numpy as np
#from pyDOE import lhs
#from scipy.stats.distributions import norm, truncnorm, lognorm, uniform
#import matplotlib.pyplot as plt
#import subprocess
import pandas as pd
#import os
#from datetime import datetime
from  .toolkit.tools import errorMessage, createFolder
from .model import Simulator

class Scheduler:
    def __init__(self, stdpath,results = None, models = None): #, jobs = 0):
        self.stdpath = stdpath
        #self.jobs = jobs
        if results is None:
            self.results = pd.DataFrame(data=None)
        else:
            self.results = models   
        
        if models is None:
            self.models = []
        else:
            self.models = models 
            
    def loadStudy(self):
        try:
            with open(self.stdpath, 'rb') as inp:
                self.std = pickle.load(inp)
        except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
            errorMessage(4)
            return
        
        #Create Run folder
        newpath ='\\'.join(self.stdpath.split('\\')[:-1])+'\\RUN'
        createFolder(newpath)
        
        # ID
        df = pd.DataFrame({'ID':np.arange(1,self.std.nsamples+1)})
        df = df.set_index('ID')
        
        # Parameters
        params = []
        for i,row in enumerate(self.std.parameters):
            params.append(row.pName)
            df[row.pName] = self.std.experiments[:,i]
            
        #Cases
        cases = []
        for case in self.std.cases:
            cases.append(case)
        
        # OFs
        aux = np.empty(self.std.nsamples)
        aux[:] = np.NaN
        
        for i,row in enumerate(self.std.objFuncs):
            for case in self.std.cases:
                cn = case.cName
                df[row.ofName+'_'+cn] = aux
            if row.delta == True:
                df[row.ofName+'_Delta'] = aux
                
        #Filename
        for case in self.std.cases:
            cn = case.cName
            filenames = [('%s\\%s_%05d\\%s_%s_%05d.dat' % (newpath,cn,i,self.std.stName,cn,i)) for i in np.arange(1,self.std.nsamples+1)]
            for row in filenames: #create subfolders
                createFolder('\\'.join(row.split('\\')[:-1]))               
            
            df['File'+'_'+cn] = filenames

            #Status
            df['Status'+'_'+cn] = ['Initial' for i in range(self.std.nsamples)]
            
        #Models
        models1 = []
        for case in cases:
            models2 = []
            for md in df.iterrows():
                model = Simulator(md[0],md[1]['File_'+case.cName],params,md[1][params].values)
                model.create(case.template[0])
                stt = df['Status_'+case.cName].values
                stt[md[0]-1] = model.status
                df['Status_'+case.cName] = stt
                models2.append(model)
            models1.append(models2)

        #Update results Table
        self.results = df
        self.models = models1
        
        print('Study is ready.')
        return
    
    def runStudy(self):
        cns=[]
        for case in self.std.cases:
            cns.append(case.cName)
        
        #run simulations
        stat1 = []
        stat2 = []
        for i in range(self.std.nsamples):
            (self.models[0])[i].submit()
            (self.models[0])[i].getProd()
            stat1.append((self.models[0])[i].status)
            if len(cns)>1:
                (self.models[1])[i].submit()
                (self.models[1])[i].getProd()
                stat2.append((self.models[1])[i].status)
        self.results['Status_'+cns[0]] = stat1
        if len(cns)>1:
            self.results['Status_'+cns[1]] = stat2

        #evaluate OFs
        for ofun in self.std.objFuncs:
            ofvalues = np.empty([self.std.nsamples,len(cns)])
            ofvalues[:] = np.NaN
            for i in range(self.std.nsamples):
                for j , cn in enumerate(cns):
                    ofvalues[i,j] = ofun.calc((self.models[j])[i].prod)
            for i, cn in enumerate(cns):
                self.results[ofun.ofName+'_'+cn] = ofvalues[:,i]
            if ofun.delta == True:
                if self.std.baseFirst == True:
                    self.results[ofun.ofName+'_Delta'] = ofvalues[:,1]-ofvalues[:,0]
                else:
                    self.results[ofun.ofName+'_Delta'] = ofvalues[:,0]-ofvalues[:,1]
        return
    
    # Save Results                
    def save(self):
        with open(self.stdpath.replace('study.cls','results.cls'), 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)            
            