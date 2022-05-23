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

## Carregando os dados

# Conectando com o banco de dados
conn = sqlite3.connect("imdb.db")

# Extrai a lista das tabelas
tabelas = pd.read_sql_query("SELECT NAME AS 'Table_Name' FROM sqlite_master WHERE type = 'table'", conn)

# Visualiza o resultado
print(tabelas.head())

# Convertendo o dataframe em lista
tabelas = tabelas["Table_Name"].values.tolist()

# Percorrendo a lista  de tabelas no banco de dados e extraindo o esquema de cada uma
for tabela in tabelas:
    consulta = "PRAGMA TABLE_INFO({})".format(tabela)
    resultado = pd.read_sql_query(consulta, conn)
    print("Esquema da tabela: ", tabela)
    print(resultado)
    print("-"*100)
    print("\n")

## 1 - Quais as categorias de filme mais comuns?

# Cria consulta SQL
consulta1 = '''SELECT type, COUNT (*) AS COUNT FROM titles GROUP BY type'''

# Extrai o resultado
resultado1 = pd.read_sql_query(consulta1, conn)


# Calculando o percentual
resultado1['Percentual'] = (resultado1['COUNT'] / resultado1["COUNT"].sum()) * 100

# Visualiza o resultado
print(resultado1)

# Criando grafico com apenas 4 categorias

# Cria Dicionario vazio
others = {}

# Filtra  o percentual em 6% e soma o total
others["COUNT"] = resultado1[resultado1["Percentual"] < 5]['COUNT'].sum

# Grava o percentual
others["Percentual"] = resultado1[resultado1["Percentual"] < 5]["Percentual"].sum()

# Ajusta o nome
others['type'] = 'others'

print(others)

# Filtra o dataframe de outras categorias
resultado1 = resultado1[resultado1["Percentual"] > 6]

# Append com o dataframe de outras categorias
resultado1 = resultado1.append(others, ignore_index= True)

# Ordena o resultado
resultado1 = resultado1.sort_values(by = "Percentual", ascending = False)

print(resultado1.head)

# Ajusta as labels
labels = [str(resultado1['type'][i])+' '+'('+str(round(resultado1["Percentual"][i], 2))+'%'+')' for i in resultado1.index]

# Plot

cs = cm.Set3(np.arange(100))

# Cria a figura
f = plt.figure(layout='constrained')

# Pie plot
plt.pie(resultado1["Percentual"], labeldistance=1, radius=2, colors=cs, wedgeprops=dict(width=0.5))
plt.legend(labels=labels, loc='center', prop={'size':12})
plt.title("Distribuição de Títulos", loc="center", fontdict={'fontsize':20, 'fontweight':20})
plt.show(block=False)


# 3 - Qual a mediana de avaliação dos filmes?

# Consulta SQL
consulta3 = '''SELECT rating, genres FROM ratings JOIN titles ON ratings.title_id = titles.title_id WHERE premiered <= 2022 AND type = 'movie' '''

# Resultado
resultado3 = pd.read_sql_query(consulta3, conn)

# Função para retornar generos
def retorna_generos(df):
    df['genres'] = df['genres'].str.lower().values
    temp = df['genres'].dropna()
    vetor = CountVectorizer(token_pattern = '(?u)\\b[\\w-]+\\b', analyzer = 'word').fit(temp)
    generos_unicos = vetor.get_feature_names()
    generos_unicos = [genre for genre in generos_unicos if len(genre) > 1]
    return generos_unicos

# Cria listas vazias para armazenamento
genero_counts = []
genero_ratings = []

# Loop
for item in generos_unicos:
    # Retorna o valor  de filmes por genero
    consulta ='SELECT COUNT(rating) FROM ratings JOIN titles ON ratings.title_id=titles.title_id WHERE genres LIKE ' + '\'' + '%' + item + '%' + '\' AND type=\'movie\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_counts.append(resultado.values[0][0])

    # Retorna a avaliação de filmes por genero
    consulta = 'SELECT rating FROM ratings JOIN titles ON ratings.title_id=titles.title_id WHERE genres LIKE ' + '\'' + '%' + item + '%' + '\' AND type=\'movie\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_ratings.append(np.median(resultado['rating']))

# Prepara o DataFrame
df_generos_ratings = pd.DataFrame()
df_generos_ratings['genres'] = generos_unicos
df_generos_ratings['count'] = genero_counts
df_generos_ratings['rating'] = genero_ratings

print(df_generos_ratings)

