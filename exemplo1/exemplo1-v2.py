"""
exemplo1-v2.py — API REST Simples de Listagem de Produtos com Flask
====================================================================

Este arquivo cria um webservice mínimo usando a biblioteca Flask do Python.
Um webservice é um programa que fica "escutando" requisições HTTP — o mesmo
tipo de comunicação que um navegador usa para acessar sites — e devolve
respostas padronizadas.

Este exemplo implementa apenas UMA operação:
  - Listar todos os produtos → GET /produtos

Os dados ficam armazenados diretamente no código (em memória), sem banco
de dados, o que é ideal para aprender os conceitos básicos antes de
adicionar persistência real.

Diferença em relação à v1:
  A v1 retornava os dados como texto puro. Esta v2 utiliza jsonify para
  retornar os dados em formato JSON — o padrão de troca de dados de APIs
  modernas — e inclui o código de status HTTP explicitamente (200 OK).

Como executar:
  python exemplo1-v2.py

O servidor ficará disponível em: http://127.0.0.1:5000
Para ver os produtos, acesse: http://127.0.0.1:5000/produtos
"""

# ---------------------------------------------------------------------------
# IMPORTAÇÕES
# ---------------------------------------------------------------------------
# Flask   → framework (conjunto de ferramentas) que transforma este script
#           em um servidor web capaz de receber e responder requisições HTTP.
# jsonify → função do Flask que converte listas e dicionários Python para
#           o formato JSON e configura automaticamente o cabeçalho da
#           resposta como "Content-Type: application/json".
from flask import Flask, jsonify

# ---------------------------------------------------------------------------
# CRIAÇÃO DA APLICAÇÃO
# ---------------------------------------------------------------------------
# Flask(__name__) cria a instância principal do servidor web.
# __name__ é uma variável especial do Python que contém o nome do módulo
# atual. O Flask usa esse valor para localizar arquivos e configurações.
app = Flask(__name__)

# ---------------------------------------------------------------------------
# "BANCO DE DADOS" EM MEMÓRIA
# ---------------------------------------------------------------------------
# Em vez de um banco de dados real, usamos uma lista de dicionários Python.
# Cada dicionário representa um produto com três campos: id, nome e preco.
# Importante: esses dados existem apenas enquanto o servidor está rodando.
# Ao reiniciar o programa, a lista volta ao estado original definido aqui.
produtos = [
    {"id": 1, "nome": "Notebook",  "preco": 3500.00},
    {"id": 2, "nome": "Mouse",     "preco": 80.00},
    {"id": 3, "nome": "Teclado",   "preco": 150.00},
]


# ---------------------------------------------------------------------------
# ROTA DA API
# ---------------------------------------------------------------------------
# Uma "rota" define qual URL + método HTTP aciona qual função Python.
# O decorador @app.route() faz essa ligação:
#   - "/produtos"     → caminho da URL após o endereço do servidor
#   - methods=["GET"] → aceita apenas requisições do tipo GET
#                       (consulta de dados, sem modificar nada)
#
# Ao acessar http://127.0.0.1:5000/produtos com o método GET,
# o Flask automaticamente chama a função listar_produtos().
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    """
    Retorna a lista completa de produtos em formato JSON.

    Endpoint : GET /produtos
    Resposta : Lista JSON com todos os produtos e status HTTP 200 (OK).

    O código de status HTTP 200 significa "OK" — a requisição foi
    processada com sucesso e a resposta contém o resultado esperado.

    Exemplo de resposta:
        [
            {"id": 1, "nome": "Notebook", "preco": 3500.0},
            {"id": 2, "nome": "Mouse",    "preco": 80.0},
            {"id": 3, "nome": "Teclado",  "preco": 150.0}
        ]
    """
    # jsonify(produtos) converte a lista Python em JSON.
    # O segundo valor (200) é o código de status HTTP retornado ao cliente.
    return jsonify(produtos), 200


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA
# ---------------------------------------------------------------------------
# if __name__ == "__main__" garante que o servidor só seja iniciado quando
# este arquivo for executado diretamente (python exemplo1-v2.py).
# Se outro arquivo importar este módulo, o bloco abaixo NÃO será executado,
# evitando que o servidor suba de forma indesejada.
#
# Parâmetros do app.run():
#   debug=True → modo de depuração: recarrega o servidor automaticamente ao
#                salvar o arquivo e exibe erros detalhados no terminal.
#                NUNCA use debug=True em produção (expõe informações internas).
#   port=5000  → porta TCP em que o servidor escutará conexões.
#                Acesso via: http://127.0.0.1:5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
