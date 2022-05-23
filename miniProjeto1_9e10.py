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


## 9 - Quais são os Top 10 melhores filmes?
# Top 10 filmes com melhor avaliação e mais de 25 mil votos

# Consulta SQL
consulta9 = '''
            SELECT primary_title AS Movie_Name, genres, rating
            FROM titles JOIN ratings ON titles.title_id=ratings.title_id
            WHERE titles.type = 'movie' AND ratings.votes >= 25000
            ORDER BY rating DESC
            LIMIT 10'''

# Resultado
resultado9 = pd.read_sql_query(consulta9, conn)

#Top 10 melhores filmes
print('\nOs 10 melhores filmes','\n\n',resultado9)


## 10 - Quais são os Top 10 piores filmes?
# Top 10 filmes com pior avaliação e mais de 25 mil votos

# Consulta SQL
consulta10 = '''
            SELECT primary_title AS Movie_Name, genres, rating
            FROM titles JOIN ratings ON titles.title_id=ratings.title_id
            WHERE titles.type = 'movie' AND ratings.votes >= 25000
            ORDER BY rating ASC
            LIMIT 10'''

# Resultado
resultado10 = pd.read_sql_query(consulta10, conn)

#Top 10 piores filmes
print('\nOs 10 piores filmes','\n\n',resultado10)