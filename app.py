import math
import numpy as np
from math import e
from flask import Flask, flash, redirect, render_template, json, request, session, abort, jsonify
from livereload import Server
import json
from urllib.parse import parse_qs

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
    resultado_matrix, matriz_final, passos, sucesso, matrix_original = preencherMatriz(
        int(matriz_json["qtd"]), matriz_json)
    print(passos)

    return render_template('solucao.html', original=matrix_original, final=matriz_final, passos=passos)


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

    resultado_matrix, matriz_final, passos, sucesso = EliminacaoGauu(
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
    # print(resultado_matrix)
    print(matriz_final)
    # print(passos)
    # print(sucesso)
    return resultado_matrix, final_front_end, passos, sucesso, original_front_end


def EliminacaoGauu(qtd_linhas, matrix):
    linhas = qtd_linhas
    colunas = linhas + 1
    length = linhas * (linhas+1)
    passos = []
    for linha_pivo in range(linhas-1):
        for linha in range(linha_pivo+1, linhas):
            pivo = matrix[linha_pivo][linha_pivo]
            if pivo == 0:
                if (linha_pivo+1 < linhas-1) and matrix[linha_pivo + 1][linha_pivo] != 0:
                    linhaAnterior = matrix[linha_pivo]
                    linhaPosterior = matrix[linha_pivo + 1]
                    print('Anterior', linhaAnterior)
                    print('Posterior', linhaPosterior)
                    matrix[linha_pivo + 1] = linhaAnterior
                    matrix[linha_pivo] = linhaPosterior
            print(matrix)
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
        return ans, matrix, passos, True
    except:
        return "Não é possivel resolver a matriz", matrix, passos, False


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
