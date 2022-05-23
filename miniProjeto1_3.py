## Carregando Pacotes

from operator import index
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

# Cria consulta SQL
consulta2 = '''SELECT genres, COUNT(*) FROM titles WHERE type = 'movie' GROUP BY genres'''

# Resultado
resultado2 = pd.read_sql_query(consulta2, conn)

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

## 3 - Qual a mediana de avaliação dos filmes?

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

# Drop do indice 18 (news) e indice 19 (n) pois não queremos essa informação
df_generos_ratings = df_generos_ratings.drop(index = 18)
df_generos_ratings = df_generos_ratings.drop(index = 19)

# Ordenar os resultados
df_generos_ratings = df_generos_ratings.sort_values(by='rating', ascending=False)

# Plot
plt.figure(figsize = (16, 10))
sns.barplot(y = df_generos_ratings.genres, x = df_generos_ratings.rating, orient = 'h')
for i in range(len(df_generos_ratings.index)):
    plt.text(4.0, i+0.25, str(df_generos_ratings['count'][df_generos_ratings.index[i]]) + ' filmes')
    plt.text(df_generos_ratings.rating[df_generos_ratings.index[i]], i+0.25, round(df_generos_ratings['rating'][df_generos_ratings.index[i]], 2))

plt.ylabel("Gênero")
plt.xlabel("Avaliação")
plt.title("\nMediana da Avaliação por Gênero\n")
plt.show()