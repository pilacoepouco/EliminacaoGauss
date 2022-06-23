import math
import numpy as np
from math import e
from flask import Flask, flash, redirect, render_template, json, request, session, abort, jsonify
from livereload import Server
import json
from urllib.parse import parse_qs
import scipy.linalg

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/solution')
def solution():
    query_decode = request.query_string.decode()
    # valor_params = json.dumps(parse_qs(query_decode))
    matriz = {x.split('=')[0]: int(x.split('=')[1])
              for x in query_decode.split("&")}
    matriz_string = json.dumps(matriz)
    matriz_json = json.loads(matriz_string)
    resultado_matrix, matriz_final, passos, sucesso, matrix_original, identidade_front_end, resultadoLu = preencherMatriz(
        int(matriz_json["qtd"]), matriz_json)
    print(passos)

    return render_template('solucao.html', original=matrix_original, final=matriz_final, passos=passos, identidade=identidade_front_end)


def preencherMatriz(qtd_linhas, matriz_datas):
    linhas = qtd_linhas
    colunas = linhas + 1
    length = linhas * (linhas+1)
    matrix = np.arange(length).reshape(linhas, colunas)+1
    for linha in range(linhas):
        for coluna in range(colunas):
            if coluna == colunas-1:
                matrix[linha][coluna] = float(matriz_datas[f'b{linha+1}'])
            else:
                matrix[linha][coluna] = float(
                    matriz_datas[f'a{linha+1}{coluna+1}'])
    matrix_original = matrix
    matrix = matrix.astype(np.float)
    original_front_end = ""
    # a & b & c \\ c & d & e \\c & d & e
    for linha in range(linhas):
        separator = "&"
        string_ints = [str(int) for int in matrix_original[linha]]
        separator = separator.join(string_ints)
        if linha == 0:
            original_front_end += separator
        else:
            original_front_end += " \\\ " + separator
    a = np.array([line[:-1] for line in matrix_original])
    b = [line[-1] for line in matrix_original]

    resultado_matrix, matriz_final, passos, sucesso, indentidade = EliminacaoGauu(
        qtd_linhas, matrix)

    final_front_end = ""
    # a & b & c \\ c & d & e \\c & d & e
    for linha in range(linhas):
        separator = "&"
        string_ints = [str(int) for int in matriz_final[linha]]
        separator = separator.join(string_ints)
        if linha == 0:
            final_front_end += separator
        else:
            final_front_end += " \\\ " + separator

    identidade_front_end = ""
    # a & b & c \\ c & d & e \\c & d & e
    for linha in range(linhas):
        separator = "&"
        string_ints = [str(int) for int in indentidade[linha]]
        separator = separator.join(string_ints)
        if linha == 0:
            identidade_front_end += separator
        else:
            identidade_front_end += " \\\ " + separator
    # print(resultado_matrix)
    # print(passos)
    # print(sucesso)
    resultadoLu = LU(a, b)

    return resultado_matrix, final_front_end, passos, sucesso, original_front_end, identidade_front_end, resultadoLu


def EliminacaoGauu(qtd_linhas, matrix):
    linhas = qtd_linhas
    colunas = linhas + 1
    length = linhas * (linhas+1)
    passos = []
    indentidade = np.eye(qtd_linhas)
    for linha_pivo in range(linhas-1):
        for linha in range(linha_pivo+1, linhas):
            pivo = matrix[linha_pivo][linha_pivo]
            if pivo == 0.0:
                if (linha_pivo+1 <= linhas-1) and matrix[linha_pivo + 1][linha_pivo] != 0:
                    # listaAux = b[inicio].copy()  # <= aqui: cria uma cópia
                    # b[inicio] = b[final]
                    # b[final] = listaAux
                    linhaAnterior = matrix[linha_pivo].copy()
                    identidadeAnterior = indentidade[linha_pivo].copy()
                    # POSTE = matrix[linha_pivo + 1].copy()
                    matrix[linha_pivo] = matrix[linha_pivo + 1]
                    matrix[linha_pivo + 1] = linhaAnterior
                    pivo = matrix[linha_pivo][linha_pivo]

                    indentidade[linha_pivo] = indentidade[linha_pivo + 1]
                    indentidade[linha_pivo + 1] = identidadeAnterior
                    passo = f'(Troca L{(linha_pivo+1)+1}  por  L{linha_pivo+1})'
                    passos.append(passo)
            multi = matrix[linha][linha_pivo] / pivo
            for coluna in range(linha_pivo+1, colunas):
                matrix[linha][coluna] = matrix[linha][coluna] - \
                    (multi*matrix[linha_pivo][coluna])
                passo = f'A({linha},{coluna}) = {matrix[linha][coluna]} - ({multi}*{matrix[linha_pivo][coluna]})'
                passos.append(passo)
            matrix[linha][linha_pivo] = matrix[linha][linha_pivo] - \
                (multi*matrix[linha_pivo][linha_pivo])
            passo = f'A({linha},{linha_pivo}) = {matrix[linha][linha_pivo]} - ({multi}*{matrix[linha_pivo][linha_pivo]})'
            passos.append(passo)
    a = np.array([line[:-1] for line in matrix])
    b = [line[-1] for line in matrix]
    try:
        ans = np.linalg.solve(a, b)
        return ans, matrix, passos, True, indentidade
    except:
        return "Não é possivel resolver a matriz", matrix, passos, False, indentidade


def LU(A, b):
    L, U = scipy.linalg.lu(A, permute_l=True)
    print(L)
    print(U)
    y = scipy.linalg.solve(L, b)
    x = scipy.linalg.solve_triangular(U, y)
    return x

# matriz_string = '{"qtd": "2", "a11": "2", "a12": "5", "b1": "9", "a21": "10", "a22": "8", "b2": "8"}'
# # the result is a Python dictionary:
# matriz = json.loads(matriz_string)
# preencherMatriz(int(matriz["qtd"]), matriz)


@app.route('/calcular', methods=["POST", "GET"])
def montarMatriz():
    if request.method == "POST":
        data_json = request.get_json()
        qtd = data_json["qtd"]
        # matriz = json.loads(data_json)
        print(type(data_json))
        # preencherMatriz(int(qtd), matriz)
        # print(matriz)
        # print('data', matriz)
    return render_template('solucao.html')
    #     # return json.dumps({'message': 'User criado com sucesso!'})
    #     # print(request)


if __name__ == "__main__":
    server = Server(app.wsgi_app)
    server.serve()
