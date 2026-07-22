from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3 
from flask import Flask, request

app = Flask(__name__)

# Função para postar dados no banco de dados
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
               senha TEXT NOT NULL
                  )
   """)

    cursor.execute('INSERT INTO contas (email, senha) VALUES (?, ?)',
                  (email,senha))


    conexao.commit()
    conexao.close()
    return jsonify({"mensagem":"Conta criado com sucesso"})


#Função para pegar os dados
@app.route("/contas", methods=["POST"])
def get_data():
    dados = request.get_json()
    email = dados['email']
    senha = dados['senha']
    conexcao = sqlite3.connect("requis.db")
    cursor = conexcao.cursor()
    cursor.execute("SELECT * FROM contas WHERE email = ?",(email,))
    resultado = cursor.fetchall()
    if not resultado :
        return jsonify({
            'Sucesso':False,
            'Mensagem':'Email não encontrado'})
    elif resultado[0] != senha:
        return jsonify({
            'Sucesso':False,
            'Mensagem':'Senha incorreta'
        })
    conexcao.close()
    # Pegar os dados que foram colocados no login comparar se é compativel com alguma senha salva no banco de dados logo após exluir
    return jsonify({
        "Sucesso": True,
        'Mensagem':'Login realizado com sucesso'
    })


app.run(debug=True)
CORS(app)
# A segurança das contas vai utilizar um sistema basico hash de senha