"""
exemplo2-v2.py — API REST de Gerenciamento de Produtos com Flask
=================================================================

Este arquivo implementa um webservice (serviço web) completo utilizando
a biblioteca Flask do Python. Um webservice é um programa que roda no
servidor e responde a requisições HTTP — como as que um navegador ou
aplicativo fazem ao acessar uma URL.

O webservice segue o padrão CRUD:
  - C (Create)  → criar um novo produto        [POST]
  - R (Read)    → ler/listar produto(s)         [GET]
  - U (Update)  → atualizar um produto          [PUT]
  - D (Delete)  → remover um produto            [DELETE]

Os dados são mantidos em memória (uma lista Python), o que significa
que são perdidos quando o servidor é reiniciado — ideal para exemplos
e prototipagem.

Como executar:
  python exemplo2-v2.py

O servidor ficará disponível em: http://127.0.0.1:5000
"""

# ---------------------------------------------------------------------------
# IMPORTAÇÕES
# ---------------------------------------------------------------------------
# Flask  → framework que transforma este script em um servidor web.
# jsonify → converte dicionários/listas Python em respostas no formato JSON
#           (o "idioma" padrão de troca de dados entre APIs).
# request → objeto que contém os dados enviados pelo cliente na requisição
#            (ex.: o corpo de um POST com os dados do novo produto).
from flask import Flask, jsonify, request

# ---------------------------------------------------------------------------
# CRIAÇÃO DA APLICAÇÃO
# ---------------------------------------------------------------------------
# Flask(__name__) cria a instância principal da aplicação.
# __name__ é uma variável especial do Python que contém o nome do módulo
# atual; o Flask usa isso para localizar arquivos estáticos e templates.
app = Flask(__name__)

# ---------------------------------------------------------------------------
# "BANCO DE DADOS" EM MEMÓRIA
# ---------------------------------------------------------------------------
# Em vez de um banco de dados real (MySQL, PostgreSQL, etc.), usamos uma
# lista de dicionários Python. Cada dicionário representa um produto com
# quatro campos: id, nome, preco e quantidade.
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00, "quantidade": 10},
    {"id": 2, "nome": "Mouse",    "preco": 80.00,   "quantidade": 50},
    {"id": 3, "nome": "Teclado",  "preco": 150.00,  "quantidade": 30},
]

# Variável global que controla qual será o próximo ID gerado.
# Começa em 4 porque os três produtos acima já ocuparam os IDs 1, 2 e 3.
# A palavra-chave "global" (usada nas funções abaixo) permite que funções
# internas leiam E modifiquem esta variável — sem ela, a função criaria
# uma cópia local e o valor original não seria atualizado.
proximo_id = 4


# ---------------------------------------------------------------------------
# FUNÇÃO AUXILIAR
# ---------------------------------------------------------------------------
def buscar_produto(id):
    """
    Procura um produto na lista pelo seu ID.

    Parâmetros:
        id (int): O identificador numérico do produto a ser localizado.

    Retorno:
        dict  → o dicionário do produto, se encontrado.
        None  → se nenhum produto possuir o ID informado.

    Como funciona:
        Percorre cada item da lista 'produtos'. Ao encontrar um produto
        cujo campo "id" seja igual ao parâmetro recebido, retorna esse
        produto imediatamente. Se o laço terminar sem encontrar nada,
        retorna None (equivalente a "nada" em Python).
    """
    for produto in produtos:
        if produto["id"] == id:
            return produto
    return None


# ---------------------------------------------------------------------------
# ROTAS DA API
# ---------------------------------------------------------------------------
# Uma "rota" define qual URL + método HTTP aciona qual função Python.
# O decorador @app.route("caminho", methods=["MÉTODO"]) faz essa ligação.
# ---------------------------------------------------------------------------


# GET /produtos — lista todos os produtos
# ----------------------------------------
# Método HTTP GET: usado para CONSULTAR dados sem alterá-los.
# Retorna a lista completa de produtos em formato JSON com código 200 (OK).
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    """
    Retorna todos os produtos cadastrados.

    Endpoint : GET /produtos
    Resposta : Lista JSON com todos os produtos e status HTTP 200.

    Exemplo de resposta:
        [
            {"id": 1, "nome": "Notebook", "preco": 3500.0, "quantidade": 10},
            {"id": 2, "nome": "Mouse",    "preco": 80.0,   "quantidade": 50},
            ...
        ]
    """
    return jsonify(produtos), 200


# GET /produtos/<id> — busca um produto pelo ID
# -----------------------------------------------
# <int:id> é um parâmetro dinâmico na URL. O Flask extrai o número
# da URL automaticamente e o passa como argumento para a função.
# Ex.: GET /produtos/2  → id = 2
@app.route("/produtos/<int:id>", methods=["GET"])
def obter_produto(id):
    """
    Retorna um único produto identificado pelo seu ID.

    Endpoint  : GET /produtos/<id>
    Parâmetro : id (int) — parte da URL, ex.: /produtos/2
    Respostas :
        200 OK         → produto encontrado, retorna seus dados em JSON.
        404 Not Found  → nenhum produto com o ID informado existe.

    Exemplo de resposta (200):
        {"id": 2, "nome": "Mouse", "preco": 80.0, "quantidade": 50}

    Exemplo de resposta (404):
        {"erro": "Produto não encontrado"}
    """
    produto = buscar_produto(id)
    if produto is None:
        # Código 404 = "Não Encontrado" — padrão HTTP para recurso inexistente.
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify(produto), 200


# POST /produtos — cria um novo produto
# ----------------------------------------
# Método HTTP POST: usado para CRIAR um novo recurso.
# O cliente envia os dados do produto no corpo da requisição em JSON.
@app.route("/produtos", methods=["POST"])
def criar_produto():
    """
    Cria e cadastra um novo produto na lista.

    Endpoint : POST /produtos
    Corpo    : JSON com os campos obrigatórios "nome", "preco" e "quantidade".

    Exemplo de corpo da requisição:
        {
            "nome": "Monitor",
            "preco": 1200.00,
            "quantidade": 5
        }

    Respostas:
        201 Created      → produto criado com sucesso, retorna o novo produto.
        400 Bad Request  → corpo da requisição ausente ou campo obrigatório faltando.

    Observação sobre "global":
        A variável proximo_id está declarada fora desta função.
        Para poder alterá-la aqui dentro, precisamos declará-la como "global".
    """
    global proximo_id  # Informa ao Python que vamos modificar a variável global.

    # request.get_json() lê e interpreta o corpo da requisição como JSON.
    # Se o corpo estiver vazio ou mal formatado, retorna None.
    dados = request.get_json()

    if not dados:
        # Código 400 = "Bad Request" — o cliente enviou algo inválido.
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    # Valida se todos os campos obrigatórios estão presentes no JSON recebido.
    campos_obrigatorios = ["nome", "preco", "quantidade"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            # f-string: forma de inserir variáveis diretamente em textos.
            return jsonify({"erro": f"Campo obrigatório ausente: {campo}"}), 400

    # Monta o dicionário do novo produto com o próximo ID disponível.
    novo_produto = {
        "id": proximo_id,
        "nome": dados["nome"],
        "preco": dados["preco"],
        "quantidade": dados["quantidade"],
    }

    produtos.append(novo_produto)  # Adiciona o novo produto à lista.
    proximo_id += 1                # Incrementa o contador para o próximo cadastro.

    # Código 201 = "Created" — padrão HTTP para indicar criação bem-sucedida.
    return jsonify(novo_produto), 201


# PUT /produtos/<id> — atualiza um produto existente
# ----------------------------------------------------
# Método HTTP PUT: usado para ATUALIZAR um recurso existente.
# Apenas os campos enviados no corpo serão atualizados; os demais
# permanecem com seus valores originais (atualização parcial/seletiva).
@app.route("/produtos/<int:id>", methods=["PUT"])
def atualizar_produto(id):
    """
    Atualiza os dados de um produto existente.

    Endpoint  : PUT /produtos/<id>
    Parâmetro : id (int) — ID do produto a ser atualizado (na URL).
    Corpo     : JSON com um ou mais campos: "nome", "preco", "quantidade".
                Apenas os campos presentes serão alterados.

    Exemplo de corpo da requisição (atualiza só o preço):
        {"preco": 90.00}

    Respostas:
        200 OK         → produto atualizado, retorna os dados atualizados.
        400 Bad Request → corpo da requisição ausente ou inválido.
        404 Not Found  → produto com o ID informado não existe.
    """
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Corpo da requisição inválido"}), 400

    # Atualiza apenas os campos que foram enviados pelo cliente.
    # Isso permite alterar nome, preço ou quantidade individualmente.
    if "nome" in dados:
        produto["nome"] = dados["nome"]
    if "preco" in dados:
        produto["preco"] = dados["preco"]
    if "quantidade" in dados:
        produto["quantidade"] = dados["quantidade"]

    return jsonify(produto), 200


# DELETE /produtos/<id> — remove um produto
# ------------------------------------------
# Método HTTP DELETE: usado para REMOVER um recurso.
@app.route("/produtos/<int:id>", methods=["DELETE"])
def deletar_produto(id):
    """
    Remove um produto da lista pelo seu ID.

    Endpoint  : DELETE /produtos/<id>
    Parâmetro : id (int) — ID do produto a ser removido (na URL).

    Respostas:
        200 OK        → produto removido com sucesso, retorna mensagem de confirmação.
        404 Not Found → produto com o ID informado não existe.

    Exemplo de resposta (200):
        {"mensagem": "Produto 2 removido com sucesso"}
    """
    produto = buscar_produto(id)
    if produto is None:
        return jsonify({"erro": "Produto não encontrado"}), 404

    # list.remove(item) remove a primeira ocorrência do item na lista.
    produtos.remove(produto)
    return jsonify({"mensagem": f"Produto {id} removido com sucesso"}), 200


# ---------------------------------------------------------------------------
# PONTO DE ENTRADA
# ---------------------------------------------------------------------------
# if __name__ == "__main__" garante que o servidor só seja iniciado quando
# este arquivo for executado diretamente (python exemplo2-v2.py).
# Se outro arquivo importar este módulo, o servidor NÃO será iniciado
# automaticamente — evitando efeitos colaterais indesejados.
#
# Parâmetros do app.run():
#   debug=True  → ativa o modo de depuração: recarrega o servidor
#                 automaticamente ao salvar o arquivo e exibe erros
#                 detalhados no navegador. NÃO usar em produção.
#   port=5000   → define a porta TCP em que o servidor escutará.
#                 Acesso via: http://127.0.0.1:5000
if __name__ == "__main__":
    app.run(debug=True, port=5000)
