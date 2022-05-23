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


## 6 - Qual o filme com o maior tempo de duração? Calcule o percentil

# Consulta SQL
consulta6 = '''
            SELECT runtime_minutes Runtime FROM titles
            WHERE type = 'movie' AND Runtime != 'NaN' 
            '''

# Resultado
resultado6 = pd.read_sql_query(consulta6, conn)

# Loop para cálculo dos percentis
for i in range(101):
    val = i
    perc = round(np.percentile(resultado6['Runtime'].values, val), 2)
    print('{} percentil de duração (runtime) é: {}'.format(val, perc))

# Refazendo consulta buscando o filme de maior duração
consulta6 = '''
            SELECT primary_title, runtime_minutes Runtime FROM titles
            WHERE type = 'movie' AND Runtime != 'NaN'
            ORDER BY Runtime DESC
            LIMIT 1
            '''
# Resultado
resultado6 = pd.read_sql_query(consulta6, conn)

print('\nO filme mais longo resgistrado chama-se {} e tem uma duração de {} minutos.'.format(resultado6['primary_title'][0], resultado6['Runtime'][0]))