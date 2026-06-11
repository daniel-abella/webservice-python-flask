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
└── README.md
```

| Arquivo | O que faz |
|---|---|
| `exemplo1-v2.py` | API com um único endpoint `GET /produtos` |
| `exemplo2-v2.py` | API completa com `GET`, `POST`, `PUT` e `DELETE` |

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

---

## Dependências

| Pacote | Versão | Para que serve |
|--------|--------|----------------|
| [Flask](https://flask.palletsprojects.com/) | última estável | Framework web que cria o servidor HTTP e gerencia as rotas |

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
