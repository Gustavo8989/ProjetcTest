from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3 


from flask import Flask, request

app = Flask(__name__)

@app.route("/salvar", methods=["POST"])
def salvar_dados():
    dados = request.get_json()

    email = dados["email"]
    senha = dados["senha"]
    conexao = sqlite3.connect("requis.db")
    cursor = conexao.cursor()

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS contas(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               email TEXT NOT NULL,
               senha_hash TEXT NOT NULL
                  )
   """)

    cursor.execute('INSERT INTO contas (email, senha) VALUES (?, ?, ?)',
                  (email,senha))


    conexao.commit()
    conexao.close()

app.run(debug=True)
# A segurança das contas vai utilizar um sistema basico hash de senha