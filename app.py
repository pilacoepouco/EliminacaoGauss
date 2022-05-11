import math
import numpy as np
from math import e

linhas = 3
colunas = linhas + 1
length = linhas * (linhas+1)
matrix = np.arange(length).reshape(linhas, colunas)+1
print(matrix)

for linha in range(0, linhas):
    pivo = matrix[linha][linha]
    linha_pivo = linha
    multi = 0
    for coluna in range(linha, colunas):
        # linhaJ = coluna + 1
        if (coluna+1) < linhas:
            linhaJ = coluna + 1
            multi = matrix[linhaJ][linha] / pivo
            # for coluna_res in range(0, colunas):
            # print(matrix[linhaJ][coluna_res])
            matrix[linhaJ][linha] = matrix[linhaJ][linha] - \
                multi*matrix[linha_pivo][linha]
            # print(matrix[linhaJ][linha])
        # if linha != 0:
            # print(matrix[linha][coluna])

print(matrix)
a = np.array([line[:-1] for line in matrix])
b = [line[-1] for line in matrix]
ans = np.linalg.solve(a, b)

print(a)
print(b)
print(ans)
