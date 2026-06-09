# Identificação de spam no Email
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split 
import pandas as pd 
import numpy as np
import re

# 0 Não é Spam
# 1 É Spam

# Pegando o banco de dados e Dividindo X e Y
date = pd.read_csv("spam_ham_dataset.csv")
df = pd.DataFrame(date)
x = df.drop("label_num",axis=1)
y = df["label_num"]

# Dividindo o treino do teste

x_train,x_teste,y_train,y_teste = train_test_split(x,y,test_size=0.3)

# Criando e treinado um classificador

clf = DecisionTreeClassifier(criterion='gini', max_depth=3)
previsoes = clf.predict(x_teste)

print(previsoes)