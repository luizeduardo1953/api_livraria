
# 📚 API de Livraria com Flask, MongoDB e Autenticação JWT

Este projeto é uma API RESTful desenvolvida em Python utilizando o framework **Flask**, banco de dados **MongoDB** (MongoDB Atlas), autenticação com **JWT (JSON Web Token)** e segurança de senhas com **hashing**.  

---

## 🚀 Tecnologias Utilizadas

- [Flask](https://flask.palletsprojects.com/) – Framework web leve e flexível
- [PyMongo](https://pymongo.readthedocs.io/) – Conector MongoDB para Python
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) – Autenticação via token
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) – MongoDB na nuvem
- [Werkzeug Security](https://werkzeug.palletsprojects.com/) – Geração e verificação de senhas hash

---

## 🧩 Instalação e Execução

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/nome-do-repositorio.git
cd nome-do-repositorio
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)
python -m venv env  # Cria a pasta do ambiente virtual com o nome 'env'

# Ativar o ambiente virtual:
``` bash
source env/bin/activate     # Para Linux/macOS
env\Scripts\activate        # Para Windows (no Prompt de Comando)
. env/bin/activate          # Alternativa para alguns shells Unix/Linux

# Desativar o ambiente virtual:
deactivate
```

### 3. Instale as dependências
```bash
pip install flask pymongo flask-jwt-extended werkzeug
```

### 4. Configure sua conexão com MongoDB Atlas
Edite esta linha no seu arquivo principal:
```python
client = MongoClient('mongodb+srv://USUARIO:SENHA@seucluster.mongodb.net/?retryWrites=true&w=majority')
```

### 5. Execute a aplicação
```bash
python nome_do_arquivo.py
```

A aplicação será executada em: [http://localhost:5000](http://localhost:5000)

---

## 🔐 Autenticação JWT

### Cadastro de usuário
- **POST /cadastro**
```json
{
  "username": "teste",
  "password": "123456"
}
```

### Login
- **POST /login**
```json
{
  "username": "teste",
  "password": "123456"
}
```
- Retorna:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGci..."
}
```

### Acesso a rota protegida
- **GET /perfil**
- Cabeçalho:
```
Authorization: Bearer SEU_TOKEN
```

---

## 📚 Endpoints da API

| Método | Rota               | Descrição                     |
|--------|--------------------|-------------------------------|
| POST   | /livros            | Cadastra um novo livro        |
| GET    | /livros            | Retorna todos os livros       |
| GET    | /livros/<isbn>     | Retorna um livro específico   |
| PUT    | /livros/<isbn>     | Edita um livro                |
| DELETE | /livros/<isbn>     | Exclui um livro               |
| POST   | /cadastro          | Cria um novo usuário          |
| POST   | /login             | Autentica e retorna um token  |
| GET    | /perfil            | Acessa dados do usuário (JWT) |

---

## 🧠 Explicação das Importações

```python
from flask import Flask, jsonify, request
```
- Cria e gerencia a aplicação Flask e manipula requisições/respostas.

```python
from flask_jwt_extended import (
    create_access_token, jwt_required, JWTManager, get_jwt_identity
)
```
- Cria tokens, protege rotas e identifica usuários autenticados.

```python
from pymongo import MongoClient
```
- Conecta o app ao banco MongoDB.

```python
from bson.objectid import ObjectId
```
- Utilizado para buscar documentos pelo ID.

```python
from pymongo.errors import PyMongoError
```
- Captura e trata erros de conexão/consulta no MongoDB.

```python
from werkzeug.security import generate_password_hash, check_password_hash
```
- Garante segurança das senhas (hash e verificação).

---

## 🧪 Testando com Postman

1. **POST /cadastro**: Crie um novo usuário.
2. **POST /login**: Autentique e copie o token retornado.
3. **GET /perfil**: Use o token como **Bearer Token** no cabeçalho da requisição.

---

## 📞 Contato

Projeto desenvolvido por **Luiz Eduardo**  
✉️ E-mail: [luizeduardo1953@gmail.com]  
🐙 GitHub: [github.com/luizeduardo1953](https://github.com/luizeduardo1953)

---
