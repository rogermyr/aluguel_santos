import requests
from unidecode import unidecode
import pandas as pd
import numpy as np

# Carregando dataset
arquivo = "santos_rent.csv"
santos = pd.read_csv(arquivo)
arquivo2 = "santos_local.csv"
end = pd.read_csv(arquivo2)

santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Primeiro de Maio','1 de Maio'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('º de Maio','1 de Maio'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Rua Engenheiro Manoel Ferramenta Júnior','Manoel Ferramenta Júnior'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Matias','Mathias'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Doutor Tolentino Filgueiras','Tolentino Filgueiras'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Doutor Galeão Carvalhal','Galeão Carvalhal'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace(' xx',''))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Costa x','Costa'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('J. Menino','José Menino'))
santos['endereco'] = santos['endereco'].apply(lambda x: x.replace('Doutor Cunha','Cunha'))

data = santos.merge(end, on='endereco')
data.head()

data = data.drop(['Unnamed: 0_x','Unnamed: 0_y'] , axis = 1)
data

data.isna().sum()

data = data.dropna(how = 'any', subset=['rooms', 'bathroom'])

data.isna().sum()

import requests
from time import sleep

def get_geo(cep):
    try:
        url = "https://www.cepaberto.com/api/v3/cep?cep="
        # O seu token está visível apenas pra você
        headers = {'Authorization': 'Token token=461f19961c9388e6f3383a8504e9fd25'}
        response = requests.get(url+cep, headers=headers)
        sleep(0.5)
        x = response.json()['latitude']
        y = response.json()['longitude']
        print(x + ',' + y)
        return x + ',' + y
    except:
        print(cep)
        return np.nan

end['CEP'] = end['CEP'].astype(str)
end['CEP'] = end['CEP'].apply(lambda x: x.replace('-',''))

end['coord'] = end['CEP'].apply(lambda x: get_geo(x))

# Novo dataframe contendo os valores da geolocalização divididos em 2 colunas
new = end["coord"].str.split(",", n = 1, expand = True) 
  
# Inserindo os valores de latitude e longitude no dataframe "end"
end["lat"]= new[0] 
end["long"]= new[1] 
  
# Retirando a coluna antigas 
end.drop(columns =["coord"], inplace = True) 

end.to_csv('santos_geo.csv')  