import math
import numpy as np
from math import e
from flask import Flask, flash, redirect, render_template, json, request, session, abort, jsonify
from livereload import Server
import json

# app = Flask(__name__)


# @app.route('/')
# def main():
#     return render_template('index.html')


# @app.route('/solution')
# def solution():
#     return render_template('solucao.html')


# @app.route('/calcular', methods=["POST", "GET"])
# def montarMatriz():
#     if request.method == "POST":
#         data_json = request.get_json()
#         qtd = data_json["qtd"]
#         print(data_json)
#     return json.dumps({'message': 'User criado com sucesso!'})
#     #     # return json.dumps({'message': 'User criado com sucesso!'})
#     #     # print(request)


# if __name__ == "__main__":
#     server = Server(app.wsgi_app)
#     server.serve()


def preencherMatriz(qtd_linhas, matriz_datas):
    linhas = qtd_linhas
    colunas = linhas + 1
    length = linhas * (linhas+1)
    matrix = np.arange(length).reshape(linhas, colunas)+1
    print(matrix)


def EliminacaoGauu(qtd_linhas, matriz_param):
    linhas = 3
    colunas = linhas + 1
    length = linhas * (linhas+1)
    matrix = np.arange(length).reshape(linhas, colunas)+1
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


matriz_string = '{"qtd": "2", "a11": "32", "a12": "32", "b1": "321", "a21": "321", "a22": "312", "b2": "312"}'
# the result is a Python dictionary:
matriz = json.loads(matriz_string)
preencherMatriz(int(matriz["qtd"]), matriz)
