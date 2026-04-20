import cohere
import math


with open("key.txt") as api:
    key = api.read()

co = cohere.ClientV2(key)

menssage = []

while True:
    user_input = str(input(": "))
    menssage.append(user_input)
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role":"user","content":menssage},],
    )
    response_chat = response.message.content[0].text
    if user_input.lower() in ["quit","sair"]:
        break
    print(response_chat)
