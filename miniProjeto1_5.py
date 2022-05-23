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
from util import retorna_generos

warnings.filterwarnings("ignore")
sns.set_theme(style = "whitegrid")

# Conectando com o banco de dados
conn = sqlite3.connect("imdb.db")

# Consulta SQL
consulta5 = 'SELECT genres FROM titles'

# Resultado
resultado5 = pd.read_sql_query(consulta5, conn)

# Retorna os generos unicos
generos_unicos = retorna_generos(resultado5)

# Fazendo a contagem
genero_count = []
for item in generos_unicos:
    consulta = 'SELECT COUNT(*) COUNT FROM titles WHERE genres LIKE '+ '\''+ '%' + item + '%' + '\' AND type=\'movie\' AND premiered <= 2022'
    resultado = pd.read_sql_query(consulta, conn)
    genero_count.append(resultado['COUNT'].values[0])

# Prepara o DataFrame
df_genero_count = pd.DataFrame()
df_genero_count['genre'] = generos_unicos
df_genero_count['Count'] = genero_count

# Calcula o top 5
df_genero_count = df_genero_count.sort_values(by='Count', ascending=False)
top_generos = df_genero_count.head()['genre'].values

# Plot
plt.figure(figsize=(16,8))

# Loop e Plot
for item in top_generos:
    consulta = 'SELECT COUNT(*) Number_of_movies, premiered Year FROM titles WHERE genres LIKE '+ '\''+ '%' + item + '%' + '\' AND type=\'movie\' AND premiered <= 2022 GROUP BY Year'
    resultado = pd.read_sql_query(consulta, conn)
    plt.plot(resultado['Year'], resultado['Number_of_movies'])

plt.xlabel('\nAno')
plt.ylabel('Número de Filmes Avaliados')
plt.title('\nNúmero de Filmes Avaliados por Gênero em Relação ao Ano de Estréia\n')
plt.legend(labels = top_generos)
plt.show()