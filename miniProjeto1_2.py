## Carregando Pacotes

import re
import time
import sqlite3
from turtle import width
import pycountry
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import cm
from sklearn.feature_extraction.text import CountVectorizer
import warnings
warnings.filterwarnings("ignore")
sns.set_theme(style = "whitegrid")

# Conectando com o banco de dados
conn = sqlite3.connect("imdb.db")


## 2 - Qual o numero de titulos por gênero?

# Cria consulta SQL
consulta2 = '''SELECT genres, COUNT(*) FROM titles WHERE type = 'movie' GROUP BY genres'''

# Resultado
resultado2 = pd.read_sql_query(consulta2, conn)

print(resultado2)

# Converte as strings para minusculo
resultado2['genres'] = resultado2['genres'].str.lower().values

# Remove Nulls
temp = resultado2['genres'].dropna()

# Criando vetor através de expressão regular para filtrar as strings
padrao = '(?u)\\b[\\w-]+\\b'
vetor = CountVectorizer(token_pattern=padrao, analyzer='word').fit(temp)

# Aplica a vetorização ao dataset sem os valores NULL
bag_generos = vetor.transform(temp)

#Retorna Generos unicos
generos_unicos = vetor.get_feature_names()

# Criando o DataFrame dos generos
generos = pd.DataFrame(bag_generos.todense(), columns=generos_unicos, index=temp.index)

generos.info()

# dropando a coluna n q foi criada
generos = generos.drop(columns = 'n', axis = 0)

# Calcula o percentual
generos_percentual = 100*pd.Series(generos.sum()).sort_values(ascending=False) / generos.shape[0]

# Visualiza
generos_percentual.head(10)

# Plot
plt.figure(figsize = (16, 8))
sns.barplot(x = generos_percentual.values, y = generos_percentual.index, orient = 'h', palette = 'terrain')
plt.ylabel('Gênero')
plt.xlabel('\nNúmero de Títulos  por Gênero')
plt.show()