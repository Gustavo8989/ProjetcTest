import sqlite3 
import psycopg 



conn = psycopg.connect(
    host="localhost",
    port = 5432,
    dbname="banco",
    user="Servers",
    password="koloin009g#1"
)

print("Conectado com sucesso!")