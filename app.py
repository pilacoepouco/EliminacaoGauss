import math
import numpy as np
from math import e

linhas = 3
colunas = linhas + 1
length = linhas * (linhas+1)
matrix = np.arange(length).reshape(linhas, colunas)+1
print(matrix)

for linha_pivo in range(linhas-1):
    for linha in range(linha_pivo+1, linhas):
        pivo = matrix[linha_pivo][linha_pivo]
        multi = matrix[linha][linha_pivo] / pivo
        for coluna in range(linha_pivo+1, colunas):
            matrix[linha][coluna] = matrix[linha][coluna] - \
                multi*matrix[linha_pivo][coluna]
        matrix[linha][linha_pivo] = matrix[linha][linha_pivo] - \
            multi*matrix[linha_pivo][linha_pivo]


a = np.array([line[:-1] for line in matrix])
b = [line[-1] for line in matrix]
try:
    ans = np.linalg.solve(a, b)
    print(ans)
except:
    print("Não é possivel resolver a matriz")
