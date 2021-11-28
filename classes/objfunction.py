import numpy as np
import pandas as pd
from datetime import datetime
from  .toolkit.tools import errorMessage


## Class ObjFunction (Objective Function) 
class ObjFunction:
    def __init__(self, ofName, ini, end, delta = False):     
        self.ofName = ofName # objective function name
        self.delta = delta # if true, consider delta between two cases
        self.ini = ini #initial date
        self.end = end #end date
            

## Class Np - Cummulative oil production
class Np(ObjFunction):
    def __init__(self, ofName, ini, end, delta = False):
        super().__init__(ofName, ini, end, delta)
        pass
    
    def calc(self,df):
        selcols = [x for x in df.columns if '[OPR]' in x] 
        t = df.index.values.copy()
        t[1:] = t[1:] - df.index[:-1] #days
        #print(t)
        Np = df[selcols].sum(axis = 1)*t #multiply rate by days
        #print(Np)
        Np = Np.cumsum()
        #print(Np)
        if ((self.ini in df.index) or (self.ini == 0)) and (self.end in df.index) and (self.ini<=self.end):
            if self.ini == 0:
                return Np[self.end]
            else: 
                return Np[self.end]-Np[self.ini]
        else:
            return errorMessage(5)
        
## Class Wp - Cummulative water production
class Wp(ObjFunction):
    def __init__(self, ofName, ini, end, delta = False):
        super().__init__(ofName, ini, end, delta)
        pass
    
    def calc(self,df):
        selcols = [x for x in df.columns if '[WPR]' in x] 
        t = df.index.values.copy()
        t[1:] = t[1:] - df.index[:-1] #days
        Wp = df[selcols].sum(axis = 1)*t
        Wp = Wp.cumsum()
        if ((self.ini in df.index) or (self.ini == 0)) and (self.end in df.index) and (self.ini<=self.end):
            if self.ini == 0:
                return Wp[self.end]
            else: 
                return Wp[self.end]-Wp[self.ini]
        else:
            return errorMessage(5)
