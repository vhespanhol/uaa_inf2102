#from __future__ import with_statement
import pickle
#import numpy as np
#from pyDOE import lhs
#from scipy.stats.distributions import norm, truncnorm, lognorm, uniform
#import matplotlib.pyplot as plt
#import subprocess
#import pandas as pd
import os
#from datetime import datetime
#import plotly.express as px

def errorMessage(error):
    errorMessage = {
        1: 'name already used',
        2: 'name not found',
        3: '#Cases greater than 2',
        4: 'File/Path not found',
        5: 'Invalid date',
        6: 'Study incomplete',
        7: 'Value must be integer'
    }
    return print('Error %d: %s.' % (error,errorMessage[error]))

def createFolder(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        #print("Directory " , dirName ,  " Created ")
    #else:    
        #print("Directory " , dirName ,  " already exists")

# def saveClass(var,fname):
#     with open(fname, 'wb') as f:
#         pickle.dump(var, f, pickle.HIGHEST_PROTOCOL)
#     return

# def loadClass(fname):
#     with open(fname, 'rb') as f:
#         cls = pickle.load(f)
#     return cls