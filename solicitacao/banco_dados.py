from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3 


conexao = sqlite3.connect("requis.db")

cursor = conexao.cursor()



cursor.execute("""
CREATE TABLE IF NOT EXISTS funcionarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            senha_hash TEXT NOT NULL
               )
""")

conexao.commit()



# Pegar os dados do Javascript
# 