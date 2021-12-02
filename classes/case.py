'''
    File name: case.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''

from  .toolkit.tools import errorMessage

## Class Study
# - classe representa um caso de estudo, possuondo 
# um template de modelo associado
class Case:
    def __init__(self, cName, ftemp, template = None):     
        self.cName = cName # Case name
        self.ftemp = ftemp # template file path
        if template is None:
            self.template = [] 
        else:
            self.template = template # template model

    # Lê template do modelo associado ao caso
    def readTemp(self):
        temps = []

        for row in [self.ftemp]:
            tpl = []          
            try:
                with open(row) as file:
                    #print(row)
                    for line in file:
                        tpl.append(line)
            except EnvironmentError:
                errorMessage(4)
                return            
            temps.append(tpl)
        
        self.template = temps
        return

