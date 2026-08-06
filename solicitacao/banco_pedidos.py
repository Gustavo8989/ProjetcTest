from flask import Flask
from flask import request
import sqlite3 
import psycopg 


app = Flask(__name__)

with open("senha_teste.txt",'r') as password:
    password = password.read() 

@app.route("/salvar",methods=["POST"])
def get_pedidos():
    # Conectando         
    dados = request.get_json()
    nome = dados["nome"]
    empresa = dados["EMPRESA"]
    item = dados["ITEM"]
    unidade = dados["UNIDADE"]
    quantidade = dados["QUANTIDADE"]
    conexao = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="banco",
        user="postgres",
        password = password,

    )
    cursor = conexao.cursor()
    cursor.execute(
    """
    INSERT INTO pedidos
    (nome, empresa, item, unidade, quantidade)
    VALUES (%s, %s, %s, %s, %s)
    """,
    (nome, empresa, item, unidade, quantidade)
        )
    conexao.commit()
    cursor.close()
    conexao.close()
    


print("Conectado com sucesso!") 