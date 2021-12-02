'''
    File name: parameter.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''

import numpy as np
from scipy.stats.distributions import norm, truncnorm, lognorm, uniform


## Class Parameter
# - parâmetros do estudo de análise de incertezas
class Parameter:
    def __init__(self, pName):
        self.pName = pName
        

## Normal Distribuition        
class NormalP(Parameter):
    def __init__(self,pName, mean, stdev):
        super().__init__(pName)
        self.mean = mean
        self.stdev = stdev
    
    # gera amostras considerando a distribuição de probabilidades do parâmetro
    def applyDist(self,arr): 
        return norm(loc=self.mean, scale=self.stdev).ppf(arr)

## Uniform Distribuition    
class UniformP(Parameter):
    def __init__(self,pName, minv, maxv):
        super().__init__(pName)
        self.maxv = maxv
        self.minv = minv

    # gera amostras considerando a distribuição de probabilidades do parâmetro
    def applyDist(self,arr):
        return uniform(loc=self.minv, scale=self.maxv-self.minv).ppf(arr)
    
## Truncated Normal Dristribuition        
class TruncNormalP(Parameter):
    def __init__(self,pName, mean, stdev, minv, maxv):
        super().__init__(pName)
        self.mean = mean
        self.stdev = stdev
        self.maxv = maxv
        self.minv = minv
    
    # gera amostras considerando a distribuição de probabilidades do parâmetro
    def applyDist(self,arr):
        a = (self.minv - self.mean)/self.stdev
        b = (self.maxv - self.mean)/self.stdev
        return truncnorm(a=a, b=b, loc=self.mean, scale=self.stdev).ppf(arr)
    
## Lognormal Dristribuition        
class LognormalP(Parameter):
    def __init__(self,pName, mean, stdev):
        super().__init__(pName)
        self.mean = mean
        self.stdev = stdev
    
    # gera amostras considerando a distribuição de probabilidades do parâmetro
    def applyDist(self,arr):
        scale = np.exp(self.mean)
        return lognorm(s=self.stdev, scale=scale).ppf(arr)