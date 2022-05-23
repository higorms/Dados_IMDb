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

## 4 - Qual a mediana de avaliação dos filmes em relação ao ano de estreia?

# Consulta SQL
consulta4 = '''
SELECT rating AS Rating, premiered AS Premiered FROM ratings 
JOIN titles ON titles.title_id=ratings.title_id
WHERE premiered <= 2022 AND type = 'movie' 
ORDER BY premiered
'''

# Resultado
resultado4 = pd.read_sql_query(consulta4, conn)

# Calculando a mediana ao longo dos anos
ratings = []
for year in set(resultado4['Premiered']):
    ratings.append(np.median(resultado4[resultado4['Premiered'] == year]['Rating']))

# Lista de Anos
anos = list(set(resultado4['Premiered']))

# Plot
plt.figure(figsize = (16, 8))
plt.plot(anos, ratings)
plt.xlabel('\nAno')
plt.ylabel('/nMediana da Avaliação')
plt.title('\nMediana da Avaliação dos Filmes por Ano de Lançamento')
plt.show()

resultado4.to_csv('avaliacao_ano.csv', sep=';', index=False)