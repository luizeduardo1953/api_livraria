from flask import Flask, jsonify, request
from flask_jwt_extended import (create_access_token, jwt_required, JWTManager, get_jwt_identity)
from pymongo.errors import PyMongoError #Tratamento de erros no banco de dados Mongo
from bson.objectid import ObjectId #Buscar ID no banco de dados
from dotenv import load_dotenv #Carregar os arquivos do .env
import os

load_dotenv() #carregando as variaveis do ambiente virtual

# Lidando com senhas HASH
from werkzeug.security import generate_password_hash, check_password_hash

#CONEXAO COM BANCO DE DADOS
from pymongo import MongoClient

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
jwt = JWTManager(app) #INICIALIZANDO 

#CONECTANDO AO BANCO DE DADOS
client = MongoClient(os.getenv("MONGO_URL"))
db = client["livraria"]

#LIVROS
livros_collection = db["livros"]

#USUÁRIOS
usuarios_collection = db["usuarios"]

#Cadastrar um livro
@app.route('/livros', methods=['POST'])
def incluir_novo_livro():
    try:
        novo_livro = request.get_json()     
         
        if not livros_collection.find_one({"titulo": novo_livro['titulo']}):  
            result = livros_collection.insert_one(novo_livro)
            novo_livro['_id'] = str(result.inserted_id)
            return jsonify(novo_livro)
    
    except TypeError:
        return jsonify({"erro": "O Corpo da requisição deve ser um JSON válido!" }), 400
    except PyMongoError as e:
        return jsonify({"erro": f"Erro no banco de dados {str(e)}"}), 500
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado {str(e)}"}), 500

#Obtendo os livros cadastrados
@app.route('/livros', methods=['GET'])
def obter_livros():
    try:
        livros_cursor = livros_collection.find() #PEGA TODOS OS OBJECTID(OS LIVROS COMO UM OBJETO)
        
        lista_de_livros = [] #CRIA A LISTA DE LIVROS
        
        for livro in livros_cursor: #PERCORRE O OBJECTID OBTENDO CADA UM E TRANFORMANDO TUDO EM STRING
            livro['_id'] = str(livro['_id'])
            lista_de_livros.append(livro) #ADICIONA A LISTA CADA LIVRO JÁ PERCORRIDO
            
        return jsonify(lista_de_livros), 200 #RETORNA UM JSON 
    
    except PyMongoError as e:
        return jsonify({"erro": f"Erro no banco de dados {str(e)}"}), 500
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado {str(e)}"}), 500

#Obtendo um livro específico pelo ID
@app.route('/livros/<string:id>', methods=['GET'])
def obter_livro_id(id):
    try:
        livro = livros_collection.find_one({"_id": ObjectId(id)}) #buscando livro por ObjectId
        
        if livro: #se o livro for encontrado converte o objectId para uma string e retorna
            livro['_id'] = str(livro['_id'])
            return jsonify(livro)
        else: #se não for encontrado retorna um erro
            return jsonify({"erro": "Livro não encontrado!"})
        
    except PyMongoError as e:
        return jsonify({"erro": f"Erro no banco de dados {str(e)}"}), 500
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado {str(e)}"}), 500  

#Editando um livro específico pelo ID
@app.route('/livros/<string:id>', methods=['PUT'])
def editar_livro_id(id):
    try:
        livro_editado = request.get_json()
        
        # Remove o campo _id se estiver presente nos dados enviados
        if '_id' in livro_editado:
            del livro_editado['_id']
        
        if not livro_editado:
            return jsonify({"erro": "Dados ausentes"}), 400

        resultado = livros_collection.update_one({"_id": ObjectId(id)}, {"$set": livro_editado})
        
        if resultado.matched_count == 0:
            return jsonify({"erro": "Livro não encontrado"}), 404
        
        return jsonify({"mensagem": "Livro atualizado com sucesso!"})
            
    except PyMongoError as e:
        return jsonify({"erro": f"Erro no banco de dados {str(e)}"}), 500
    except Exception as e:
        return jsonify({"erro": f"Ocorreu um erro inesperado {str(e)}"}), 500  
    
#Excluir livro específico por ID
@app.route('/livros/<string:id>', methods=['DELETE'])
def excluir_livro_id(id):
    try:
        livro = livros_collection.find_one({"_id": ObjectId(id)})
       
        if not livro:
            return jsonify({"erro": "Livro não encontrado"}), 404
       
        resultado = livros_collection.delete_one({"_id": ObjectId(id)})
       
        if resultado.deleted_count == 1:
            return jsonify({"mensagem": "Livro excluido com sucesso!"})
        else:
            return jsonify({"mensagem": "Não foi possível excluir o livro!"}), 500
            
    except PyMongoError as e:
        return jsonify({"erro": f"Erro no banco de dados {str(e)}"})
    except Exception as e:
       return jsonify({"erro": f"Ocorreu um erro inesperado {str(e)}"})

#CADASTRO DE USUARIOS
@app.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    username = dados.get("username")
    password = dados.get("password")

    if not username or not password:
        return jsonify({"Error": "Nome de usuário e senha são obrigatórios"}), 400

    if usuarios_collection.find_one({"username" : username}, {"_id": 0}): #objeto do id criado no mongo
        return jsonify({"Error": "Usuário já existe!"}), 409
    
    password_hash = generate_password_hash(password)
    
    dados["password"] = password_hash
    
    usuarios_collection.insert_one(dados)
    
    return jsonify({
        "message": "Usuário cadastrado com sucesso!"
    }), 201
    
#AUTENTICAÇÃO
@app.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    username = dados.get("username")
    password = dados.get("password")
    
    usuario = usuarios_collection.find_one({"username": username}, {"_id" : 0})
            
    if not usuario or not check_password_hash(usuario["password"], password):
        return jsonify({"Error": "Credenciais inválidas"}), 401
    
    token = create_access_token(identity=username)
    return jsonify(access_token=token)
        
@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    usuario_logado = get_jwt_identity()
    usuario = usuarios_collection.find_one({"username" : usuario_logado}, {"_id" : 0, "password" : 0}) #retirando os campos id e password da visão
    return jsonify({"message": f"Usuário logado com sucesso! Bem-vindo, {usuario['username']}!"}), 200

app.run(port=5000,host='localhost',debug=True)
