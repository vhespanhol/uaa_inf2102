# Uncertainty Analysis Assistant

Trabalho da disciplina 'Projeto Final de Programação' (INF2102) - DI/PUC-Rio.

## Baixar repositório
```sh
cd <your_repository>
git clone https://github.com/vhespanhol/uaa_inf2102.git
```

## Pacotes necessários
```sh
numpy
subprocess
pandas
pickle
os
datetime
scipy
pyDOE
plotly
matplotlib
```

## Inicialização da interface
```sh
from classes.iua import IUA
ua01 = IUA()
ua01.initUA()
```

## Descrição dos diretórios e arquivos principais
```sh
classes: diretório com todas as classes implementadas.
UAA.ipynb: notebook com exemplo de execução de um estudo.
projects/reservoir: diretório com template e arquivos do modelo de reservatórios. 
projects/UA_INJ: diretório com exemplo de estudo.
test.ipynb: notebook com testes de métodos individuais.
test_iterface.ipynb: notebook com testes do sistema.
test: logs e casos de teste
```

Versão Python: 3.6