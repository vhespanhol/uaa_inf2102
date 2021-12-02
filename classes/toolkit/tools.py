'''
    File name: tools.py
    Author: Vitor Hespanhol Côrtes
    Date created: 12/1/2020
    Date last modified: 12/1/2020
    Python Version: 3.6
'''
import pickle
import os

# Mensagens de erro padronizadas
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

# Função para criação de diretórios
def createFolder(dirName):
    if not os.path.exists(dirName):
        os.mkdir(dirName)