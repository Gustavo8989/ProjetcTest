# LangChain
# CrewAI
from langchain.agents import create_agent
from langchain_cohere import ChatCohere
from datetime import date
import json
import os

# Criando um Agente
with open("key.txt") as api:
    key = api.read()

menssage = []
dados = {"Entrada":"",
         "mensage_user":"",
         "mensagem_cohere":""}

hoje = date.today()
data_formatada = hoje.strftime('%d/%m/%Y')
while True:
    dados["Entrada"] = data_formatada
    model = ChatCohere(model_name="command-r-plus", cohere_api_key=key)
    user_input = input(": ")
    if user_input.lower() in ["quit","sair"]:
        break
    dados["mensage_user"] = user_input
    menssage.append(user_input)
    reponse = model.invoke(menssage).text
    dados["mensagem_cohere"] = reponse
    print(reponse)


with open('dados.json', 'w', encoding='utf-8') as text:
    json.dump(dados,text,indent=4,ensure_ascii=False)