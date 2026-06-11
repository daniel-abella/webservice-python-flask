# Webservice Python — Flask

Exemplos de APIs REST construídas com Flask para fins didáticos.

---

## Pré-requisitos

- [Python 3.8+](https://www.python.org/downloads/) instalado na máquina
- Terminal (Prompt de Comando, PowerShell ou Terminal do macOS/Linux)

Verifique se o Python está instalado executando:

```bash
python --version
```

ou, em alguns sistemas:

```bash
python3 --version
```

---

## Estrutura do projeto

```
webservice-python/
├── exemplo1/
│   ├── exemplo1-v1.py        # Versão 1 — retorna texto puro
│   ├── exemplo1-v2.py        # Versão 2 — retorna JSON com status HTTP
│   └── requirements.txt      # Dependências do exemplo 1
├── exemplo2/
│   ├── exemplo2-v1.py        # Versão 1 — CRUD básico
│   ├── exemplo2-v2.py        # Versão 2 — CRUD com validações
│   └── requirements.txt      # Dependências do exemplo 2
├── exemplo3/
│   ├── exemplo3-v1.py        # CRUD com documentação Swagger via Flasgger
│   └── requirements.txt      # Dependências do exemplo 3
├── exemplo4/
│   ├── exemplo4-v1.py        # CRUD em memória
│   ├── exemplo4-v2.py        # CRUD com MySQL
│   ├── data.sql              # Script de criação da base
│   ├── postman_collection.json
│   └── requirements.txt
├── exemplo5/
│   ├── exemplo5-v1.py        # CRUD em memória
│   ├── exemplo5-v2.py        # CRUD com MySQL
│   ├── data.sql              # Script de criação da base
│   ├── postman_collection.json
│   └── requirements.txt
├── docs/
│   └── explicacao-api-rest.pdf
└── README.md
```

| Arquivo | O que faz |
|---|---|
| `exemplo1-v2.py` | API com um único endpoint `GET /produtos` |
| `exemplo2-v2.py` | API completa com `GET`, `POST`, `PUT` e `DELETE` |
| `exemplo3-v1.py` | API CRUD com interface Swagger gerada pelo Flasgger |
| `exemplo4-v2.py` | API CRUD integrada ao MySQL |
| `exemplo5-v2.py` | Segunda variação de API CRUD integrada ao MySQL |

---

## Instalação

### 1. Clone ou baixe o projeto

Se você recebeu o projeto como `.zip`, extraia em uma pasta de sua preferência.  
Se usar Git:

```bash
git clone <url-do-repositorio>
cd webservice-python
```

### 2. Crie um ambiente virtual (recomendado)

Um ambiente virtual isola as dependências deste projeto das demais instalações Python do seu computador, evitando conflitos.

```bash
python -m venv .venv
```

Ative o ambiente virtual:

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

- **Windows (Prompt de Comando):**
  ```bat
  .venv\Scripts\activate
  ```

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

> Quando o ambiente estiver ativo, você verá `(.venv)` no início da linha do terminal.

### 3. Instale as dependências

Cada exemplo possui seu próprio `requirements.txt`. Instale as dependências do exemplo que deseja executar:

**Exemplo 1:**
```bash
pip3 install -r exemplo1/requirements.txt
```

> Em alguns sistemas o comando é `pip` em vez de `pip3`. Use o que funcionar na sua máquina.

**Exemplo 2:**
```bash
pip3 install -r exemplo2/requirements.txt
```

**Exemplo 3:**
```bash
pip3 install -r exemplo3/requirements.txt
```

**Exemplo 4:**
```bash
pip3 install -r exemplo4/requirements.txt
```

**Exemplo 5:**
```bash
pip3 install -r exemplo5/requirements.txt
```

---

## Como executar

Navegue até a pasta do exemplo desejado e execute o arquivo Python:

**Exemplo 1 (listagem de produtos):**
```bash
cd exemplo1
python exemplo1-v2.py
```

**Exemplo 2 (CRUD completo):**
```bash
cd exemplo2
python exemplo2-v2.py
```

**Exemplo 3 (CRUD com Flasgger/Swagger):**
```bash
cd exemplo3
python exemplo3-v1.py
```

**Exemplo 4 (CRUD com MySQL):**
```bash
cd exemplo4
python exemplo4-v2.py
```

**Exemplo 5 (CRUD com MySQL):**
```bash
cd exemplo5
python exemplo5-v2.py
```

O terminal exibirá uma mensagem semelhante a:

```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
```

O servidor estará disponível em **http://127.0.0.1:5000**.  
Para encerrar o servidor, pressione `Ctrl + C` no terminal.

---

## Endpoints disponíveis

### Exemplo 1

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/produtos` | Lista todos os produtos |

### Exemplo 2

| Método | URL | Descrição |
|--------|-----|-----------|
| GET | `/produtos` | Lista todos os produtos |
| GET | `/produtos/<id>` | Retorna um produto pelo ID |
| POST | `/produtos` | Cria um novo produto |
| PUT | `/produtos/<id>` | Atualiza um produto existente |
| DELETE | `/produtos/<id>` | Remove um produto |

### Exemplo 3

O `exemplo3` expõe os mesmos endpoints do exemplo 2, mas com documentação
interativa gerada automaticamente:

| Recurso | URL | Descrição |
|--------|-----|-----------|
| Swagger UI | `/apidocs/` | Interface web para visualizar e testar a API |
| Especificação OpenAPI | `/apispec_1.json` | JSON da documentação gerada pelo Flasgger |

### Exemplos 4 e 5

Os `exemplo4` e `exemplo5` expõem os mesmos endpoints CRUD de produtos, com duas variações:

- `v1`: dados em memória.
- `v2`: persistência em MySQL usando o script `data.sql`.

---

## Testando a API

### Pelo navegador

Para requisições **GET**, basta abrir o endereço no navegador:

```
http://127.0.0.1:5000/produtos
```

### Pelo terminal com `curl`

```bash
# Listar todos os produtos
curl http://127.0.0.1:5000/produtos

# Buscar produto de ID 1
curl http://127.0.0.1:5000/produtos/1

# Criar um novo produto
curl -X POST http://127.0.0.1:5000/produtos \
     -H "Content-Type: application/json" \
     -d '{"nome": "Monitor", "preco": 1200.00, "quantidade": 5}'

# Atualizar o preço do produto de ID 1
curl -X PUT http://127.0.0.1:5000/produtos/1 \
     -H "Content-Type: application/json" \
     -d '{"preco": 3200.00}'

# Remover o produto de ID 2
curl -X DELETE http://127.0.0.1:5000/produtos/2
```

### Pelo Postman

Importe o arquivo `postman_collection.json` de cada exemplo diretamente no [Postman](https://www.postman.com/) para ter todas as requisições já configuradas.

### Pelo Swagger (Flasgger)

Depois de executar o `exemplo3`, abra no navegador:

```text
http://127.0.0.1:5000/apidocs/
```

Nessa tela você poderá:

- visualizar todos os endpoints documentados;
- ver exemplos de parâmetros e respostas;
- testar requisições direto pelo navegador.

---

## Dependências

| Pacote | Versão | Para que serve |
|--------|--------|----------------|
| [Flask](https://flask.palletsprojects.com/) | última estável | Framework web que cria o servidor HTTP e gerencia as rotas |
| [Flasgger](https://github.com/flasgger/flasgger) | última estável | Gera documentação Swagger/OpenAPI para aplicações Flask |
| [mysql-connector-python](https://pypi.org/project/mysql-connector-python/) | última estável | Conecta as APIs dos exemplos 4 e 5 ao MySQL |

---

## Dúvidas comuns

**`python` não é reconhecido no Windows**  
Tente usar `python3` ou verifique se o Python foi adicionado ao PATH durante a instalação.

**Porta 5000 já está em uso**  
Altere a porta no final do arquivo `.py`:
```python
app.run(debug=True, port=5001)
```

**Módulo `flask` não encontrado**  
Certifique-se de que o ambiente virtual está ativo (`(.venv)` no terminal) e execute novamente o `pip3 install` (ou `pip install`).
