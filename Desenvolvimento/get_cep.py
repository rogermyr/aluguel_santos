import requests
from unidecode import unidecode
import pandas as pd

# Carregando dataset
arquivo = "santos_rent.csv"
data = pd.read_csv(arquivo)

data = data.drop('Unnamed: 0', axis = 1)
data.drop_duplicates(subset=['rent','endereco','rooms','bathroom','parking','area'], keep = 'first', inplace = True )
data['endereco'] = data['endereco'].str.strip()

def get_cep(end, city):
    # Coletando os dados 
    try:
        session = requests.session()
        data = {'relaxation': unidecode(end) + ' '+unidecode(city),
                'TipoCep': 'LOG',
                'semelhante': 'N',
                }
        r = session.post("http://www.buscacep.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm", data, headers={'User-Agent': 'Mozilla/5.0'})
        tables = pd.read_html(r.content) # Returns list of all tables on page
        results_table = tables[0] # Select table of interest
        res = results_table[results_table['Localidade/UF:']==city]
        print(end + ': '+ res.iloc[0][3] + ' Bairro: '+ res.iloc[0][1])
        return res.iloc[0][3], res.iloc[0][1]
    except:
        print(end + ': ')
        return str('')

data['CEP'] = data.apply(lambda row: get_cep(row['endereco'],'Santos/SP'), axis = 1)

data.to_csv('santos_local.csv')