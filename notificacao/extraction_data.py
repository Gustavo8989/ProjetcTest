from datetime import date, datetime
import pandas as pd 


data_atual = date.today().strftime('%d/%m/%Y')
lista_data = [date(2026, 2, 20), date(2026, 3, 2), date(2026, 3, 27)]
data_format = [d.strftime('%d/%m/%Y') for d in lista_data]
dict_test = {
    "PV":["0000000","111111","111111"],
    "Itens":["Tela optinet 30%","Leno vermelha 40%","Bomba"],
    "Data Entrega":data_format,
    "Status":["Comprada","Comprada","Em cotação"],
}

df_test = pd.DataFrame(dict_test)

request_number = df_test["PV"]
itens = df_test["Itens"]
date_en = df_test["Data Entrega"]
status = df_test["Status"]


if date_en < data_atual:
    if status != "Comprada":
        print("Notificação para comprar")
