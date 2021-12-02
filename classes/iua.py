'''
    File name: iua.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''

import numpy as np
from datetime import datetime
from .toolkit.tools import errorMessage, createFolder
from .parameter import Parameter, NormalP, TruncNormalP, LognormalP, UniformP
from .objfunction import ObjFunction, Np, Wp
from .case import Case
from .analysis import Analysis
from .study import Study
from .scheduler import Scheduler

## Class IUA
# - interface centralizada de interação com o usuário
class IUA: #Uncertainty Analysis Assistant
    def __init__(self, name = None,key = None):
        self.name = name
        self.key = key
    
    #####################
    # Método de inicialização da Interface (UC01)
    #####################
    def initUA(self):
        now = datetime.now()
        dtstring = now.strftime('%b %d, %Y - %H:%M:%S')
        introtxt = '=================================\n'
        introtxt += 'Uncertainty Analysis Assistant\n'
        introtxt += '           v1.0\n'
        introtxt += '=================================\n'
        introtxt += dtstring+'\n'
        introtxt += '\n'
        print(introtxt)
        
        dictfunc = {1:'1: Create a study',2:'2: Run study',3:'3: Analyse data'}
        choice = input("Select an option:\n%s\n%s\n%s\notherwise: Exit\n" % (dictfunc[1],
                                                                            dictfunc[2],
                                                                            dictfunc[3]))
        try:
            print('=> Selected %s\n' % (dictfunc[int(choice)])[1:])
        except:
            print('Ending Program...\nDone.')
            return
        
        if choice == '1':
            self.createStudy()
        elif choice == '2':
            self.runScheduler()
        elif choice == '3':
            self.analyse()
        return

    #####################
    # Método para análise dos resutados (UC04)
    #####################
    def analyse(self):
        introtxt = '===============\n'
        introtxt += '  Analysis\n'
        introtxt += '===============\n'
        print(introtxt)
        fres = input("Enter study path: ")
        try:
            analysis = Analysis(fres+'\\results.cls')
            analysis.load_results()
            print('Select analysis:\n1: Histogram\n2: Crossplot\notherwhise: Exit')
            choice = input()
            
            if choice == '1':
                print('Select Objective Function:')
                for i,row in enumerate(analysis.ofs):
                    print('%d: %s' % (i,row))
                ofc = input()
                bins = input('Bins = ')
                analysis.hist(analysis.ofs[int(ofc)],int(bins))
            
            elif choice == '2':
                print('Select Parameter 1 (X-axis):')
                for i,row in enumerate(analysis.pars):
                    print('%d: %s' % (i,row))
                p1 = input()
                print('Select Parameter 2 (Y-axis):')
                for i,row in enumerate(analysis.pars):
                    print('%d: %s' % (i,row))
                p2 = input()
                print('Select Objective Function 1 (color):')
                for i,row in enumerate(analysis.ofs):
                    print('%d: %s' % (i,row))
                ofc = input()
                print('Select Objective Function 2 (size):')
                for i,row in enumerate(analysis.ofs):
                    print('%d: %s' % (i,row))
                ofsz = input()

                analysis.xPlot(analysis.pars[int(p1)],analysis.pars[int(p2)],
                            analysis.ofs[int(ofc)],analysis.ofs[int(ofsz)])             
            else:
                print('End of analysis.')
            
        except:
            print('Results Error. Please review study.')

    #####################
    # Método para execução do estudo (UC03)
    ##################### 
    def runScheduler(self):
        introtxt = '===============\n'
        introtxt += '  Scheduler\n'
        introtxt += '===============\n'
        print(introtxt)
        fsch = input("Enter study path: ")
        try:
            sch = Scheduler(fsch+'\\study.cls')
            #print('ok1')
            sch.loadStudy()
            #print('ok2')
            sch.runStudy()
            #print('ok3')
            sch.save()
            print('Results saved!')
        except:
            print('Scheduler Error. Please review study.')

    #####################
    # Método para criação e configuração do estudo (UC02)
    #####################    
    def createStudy(self):
        introtxt = '===============\n'
        introtxt += ' Study Creator\n'
        introtxt += '===============\n'
        print(introtxt)
        
        path = input("Enter study path: ")
        stdnm = input("Enter study name: ")
        nsamp = input("Enter sample size: ")
        try:
            nsamp = int(nsamp)
        except:
            errorMessage(7)
        #    return
        std0 = Study(stdnm,path,nsamp)
        try:
            createFolder(path+'\\'+stdnm)
        except:
            print('Error: Invalid path.')
            return
        
        opt = 0
        while opt!=99:
            print('\n============\nSelect an option:')
            print('0: Sample Size')
            print('1: Add Case')
            print('2: Add Parameter')
            print('3: Add Objective Function')
            print('4: Remove Case')
            print('5: Remove Parameter')
            print('6: Remove Objective Function')
            print('7: List Study')
            print('8: Save')
            opt = input("99: EXIT\n")
            print(opt)    
            if opt == '99':
                print('Ending Program...\nDone.')
                break
            elif opt == '0':
                std0.nsamples = int(input("Enter sample size: "))
            elif opt == '1': 
                casen = input('Add Case (Name):')
                ftemp = input('Case Template File:')
                c01 = Case(casen,ftemp)
                c01.readTemp()
                std0.addCase(c01)

            elif opt == '3':
                print('OF Type:\n1: Cumulative Oil')
                print('2: Cumulative Water\notherwise: Return')
                oft = input()
                if oft !='1' and oft !='2':
                    continue
                else:
                    ofn = input('Add OF (Name):')
                    ini = float(input('Initial Time:'))
                    end = float(input('End Time:'))
                    delta = input('Delta? (0 = False )')
                    if oft == '1': 
                        of = Np(ofn,ini,end,bool(int(delta)))
                        print(of.delta)
                    else:
                        of = Wp(ofn,ini,end,bool(int(delta)))
                        print(of.delta)
                    std0.addOF(of)

            elif opt == '4': 
                    casen = input('Remove Case (Name):')
                    std0.remCase(casen)
            elif opt == '5':
                    parn = input('Remove Parameter (Name):')
                    std0.remPar(parn)    
            elif opt == '6':
                    ofn = input('Remove OF (Name):')
                    std0.remOF(ofn)

            elif opt == '2':
                    print('Parameter Distribuition:\n1: Uniform')
                    print('2: Normal')
                    print('3: Truncated Normal')
                    print('4: Lognormal\notherwise: Return')
                    part = input()

                    if int(part)<=0 or int(part)>=5:
                        continue
                    elif part =='1':
                        parn = input('Parameter Name:')
                        amin = float(input('min = '))
                        amax = float(input('max = '))
                        par = UniformP(parn,amin,amax)
                        std0.addPar(par)
                    elif part =='2':
                        parn = input('Parameter Name:')
                        amean = float(input('mean = '))
                        astd = float(input('std = '))
                        par = NormalP(parn,amean,astd)
                        std0.addPar(par)
                    elif part =='3':
                        parn = input('Parameter Name:')
                        amean = float(input('mean = '))
                        astd = float(input('std = '))
                        amin = float(input('min = '))
                        amax = float(input('max = '))
                        par = TruncNormalP(parn,amean,astd,amin,amax)
                        std0.addPar(par)
                    elif part =='4':
                        parn = input('Parameter Name:')
                        amean = float(input('mean = '))
                        astd = float(input('std = '))
                        par = LognormalP(parn,amean,astd)
                        std0.addPar(par)
            elif opt == '7':
                print('Path = ',std0.path)
                print('Study Name = ',std0.stName)
                print('Sample size = ',std0.nsamples)
                print('Cases =',[x.cName for x in std0.cases])
                print('Parameters =',[x.pName for x in std0.parameters])
                print('Objective Functions =',[x.ofName for x in std0.objFuncs])
            elif opt == '8':
                try:
                    std0.designExp()
                #    print(std0.experiments)
                    std0.save()
                    print('Study Saved!!!')
                except:
                    print('Study Incomplete. Please review before saving.')
        return    