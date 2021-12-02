'''
    File name: model.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''
import numpy as np
import subprocess
import pandas as pd
from  .toolkit.tools import errorMessage

## Class Model
# - classe responsável por criar, submeter e extrair resultados.  
class Model:
    def __init__(self, idm,mName,params,parvalues,prod =None, status='Initial'):
        self.idm = idm
        self.mName = mName
        self.params = params
        self.parvalues = parvalues
        self.status = status
        if prod is None:
            self.prod = pd.DataFrame(data=None)
        else:
            self.prod = prod 
    # Cria modelo a partir do template, substituindo nomes dos parâmetros.    
    def create(self,template):
        newm = []
        for row in template:
            aux = row+''
            for i,par in enumerate(self.params):
                if '@'+par+'@' in row:
                    aux = aux.replace('@'+par+'@','%.8g' % self.parvalues[i])
            newm.append(aux)
                
        try:
            with open(self.mName, 'w') as f:
                for item in newm:
                    f.write("%s\n" % item.replace('\n',''))
                self.status = 'Created'
        except EnvironmentError: 
            errorMessage(4)
            return                  

# Classe Simulator: 
# - responsável por submeter as simulações ao simulador externo
# - classe deve ser modificada em caso de mudança de máquina (self.exe).   
# - extrai resultados ao final da simulação
class Simulator(Model):
    def __init__(self,idm,mName,params,parvalues,prod=None,status='Initial',exe = None):
        super().__init__(idm,mName,params,parvalues,prod,status)
        self.exe = r'E:\base_case\TwoFlow.exe'

    # Submete jobs ao simulador externo    
    def submit(self):
        try:
            subprocess.run([self.exe,self.mName])
            print('Model %s: Simulation done.' % self.mName.split('\\')[-1])
            self.status = 'Simulated'
        except:
            print('Model %s: Simulatition failed.' % self.mName.split('\\')[-1])
            self.status = 'Failed'
            
    # Extrai resultados ao final da simulação
    def getProd(self):
        df = pd.read_csv(self.mName.replace('.dat','.well'), skiprows=[0,1,2],sep = '\t')
        df = df.set_index('Time')
        self.status = 'Read'
        self.prod = df
        return