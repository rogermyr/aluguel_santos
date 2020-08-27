import streamlit as st
import numpy as np
import pandas as pd
import joblib

st.beta_set_page_config(
	layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
	initial_sidebar_state="expanded",  # Can be "auto", "expanded", "collapsed"
	page_title="Calculadora de Aluguel (Santos)",  # String or None. Strings get appended with "• Streamlit". 
	page_icon="icon.png",  # String, anything supported by st.image, or None.
)

model = joblib.load('model.pkl')

st.markdown("<h1 style='text-align: center; color: blue; font-weight: bold'>Calculadora de Aluguel (Santos)</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold'>Projeto desenvolvido por: <a href='https://www.linkedin.com/in/rogeriohsilva/' target= '_blank'>Rogério Henriques Silva</a></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-weight: bold'><a href='https://github.com/rogermyr/aluguel_santos' target= '_blank'>Código fonte do projeto no Github</a></p>", unsafe_allow_html=True)

with open("style.css") as f:
    st.sidebar.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)    
    
bairro = st.sidebar.selectbox("Bairro: ", ['Aparecida','Boqueirão','Campo Grande','Embaré','Gonzaga','José Menino','Marapé','Pompéia','Ponta da Praia','Vila Mathias'])
area = st.sidebar.slider("Área (m²): ", min_value=25, max_value=650, value=25, step=5)    
quartos = st.sidebar.radio("Quartos: ", np.arange(1, 5, 1))
banheiro = st.sidebar.radio("Banheiros: ", np.arange(1, 6, 1))
garagem = st.sidebar.radio("Vagas na garagem: ", np.arange(1, 5, 1))    

if not st.sidebar.button('Calcular aluguel'):
    st.markdown("<p style='text-align: justify;'>Calculadora utilizada para estimar o valor do aluguel na cidade de Santos, baseado nas caractéristicas do imóvel fornecidas.<br>Para este projeto foram considerados apenas os bairros que tiveram mais de 100 entradas após o uso do webscrapper desenvolvido.<br><br><b>Como usar:</b><br>1- Escolha as características do imóvel no menu à esquerda<br>2- Clique no botão Calcular Aluguel<br>3- O resultado será mostrado na página principal.<br><br>Obs: Foi utilizado o site <a href='https://www.vivareal.com.br' target= '_blank'>Viva Real</a> para obter os dados dos imóveis utilizados no treinamento do modelo.</p>", unsafe_allow_html=True)        
else:
    df2 = pd.DataFrame(np.array([[area,quartos,banheiro,garagem,bairro]]),
    columns=['area', 'rooms', 'bathroom', 'parking','Bairro'])
    df2['area'] = df2['area'].astype('int64')
    df2['rooms'] = df2['rooms'].astype('int64')
    df2['bathroom'] = df2['bathroom'].astype('int64')
    df2['parking'] = df2['parking'].astype('int64')    
    df2['larea'] = np.log1p(df2['area'])
    output = np.expm1(model.predict(df2))
    st.image("imagem.jpg")
    st.markdown("<h2 style='text-align: center; font-weight: bold'>O Valor estimado do Aluguel é de R$ {}</h2>".format(str(round(float(output),2))), unsafe_allow_html=True)     