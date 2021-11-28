from  .toolkit.tools import errorMessage

## Class Study
class Case:
    def __init__(self, cName, ftemp, template = None):     
        self.cName = cName # Case name
        self.ftemp = ftemp # template file path
        if template is None:
            self.template = [] 
        else:
            self.template = template # template model

    def readTemp(self):
        temps = []

        for row in [self.ftemp]:
            tpl = []          
            try:
                with open(row) as file:
                    #print(row)
                    for line in file:
                        tpl.append(line)
            except EnvironmentError: # parent of IOError, OSError *and* WindowsError where available
                errorMessage(4)
                return            
            temps.append(tpl)
        
        self.template = temps
        return
        
    # def getPar(self):
    #     pars = []
    #     for row in self.template[0]:
    #         if '@' in row:
    #             pars.append(row.split('@')[1])
    #     return pars
