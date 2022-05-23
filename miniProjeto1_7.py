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


## 7 - Qual a relação entre Duração e Gênero?

# Consulta SQL
consulta7= '''
            SELECT AVG(runtime_minutes) AS Runtime, genres FROM titles
            WHERE type = 'movie' AND runtime_minutes != 'NaN'
            GROUP BY genres
            '''

# Resultado
resultado7 = pd.read_sql_query(consulta7, conn)

# Retornando generos unicos
generos_unicos = retorna_generos(resultado7)

# Calcula tempo de duração
genero_runtime = []
for item in generos_unicos:
    consulta = 'SELECT runtime_minutes AS Runtime FROM titles WHERE genres LIKE '+ '\''+ '%' + item + '%' + '\' AND type=\'movie\' AND runtime_minutes !=\'NaN\''
    resultado = pd.read_sql_query(consulta, conn)
    genero_runtime.append(np.median(resultado['Runtime']))

# Prepara o DataFrame
df_genero_runtime = pd.DataFrame()
df_genero_runtime['genre'] = generos_unicos
df_genero_runtime['runtime'] = genero_runtime

# Dropando o genero news (indice 18)
df_genero_runtime = df_genero_runtime.drop(index=18)

# Ordenar os dados
df_genero_runtime = df_genero_runtime.sort_values(by = 'runtime', ascending = False)

# Plot
plt.figure(figsize=(16,8))

sns.barplot(y = df_genero_runtime.genre, x = df_genero_runtime.runtime, orient = 'h')

for i in range(len(df_genero_runtime.index)):
    plt.text(df_genero_runtime.runtime[df_genero_runtime.index[i]], i+0.25, round(df_genero_runtime['runtime'][df_genero_runtime.index[i]], 2))

plt.ylabel('Gênero')
plt.xlabel('\nMediana de Tempo de Duração (Minutos)')
plt.title('\nRelação Entre  Duração e Gênero\n')
plt.show()