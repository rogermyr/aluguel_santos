# Calculadora de Aluguel (Santos)

##### Demonstração: https://aluguel-santos.herokuapp.com
##### Projeto desenvolvido em Python, em conjunto com o streamlit e heroku para fazer o deploy da aplicação.
Calculadora utilizada para estimar o valor do aluguel na cidade de Santos, baseado nas caractéristicas do imóvel fornecidas.
Para este projeto foram considerados apenas os bairros que tiveram mais de 100 entradas após o uso do webscrapper desenvolvido.

##### Como usar:
- Escolha as características do imóvel no menu à esquerda
- Clique no botão Calcular Aluguel
- O resultado será mostrado na página principal.


##### Requirements.txt

* streamlit==0.65.2
* joblib==0.13.2
* pandas==0.25.3
* numpy==1.19.1
* scikit-learn==0.23.2
* xgboost==0.90

### Desenvolvimento do Projeto:
Na pasta "Desenvolvimento" possui todo o desenvolvimento do projeto, desde as ferramentas utilizadas para fazer o webscrapping até a criação do arquivo com o modelo já treinado a ser utilizado no nosso deploy.
#
Todo o desenvolvimento pode ser acompanhado através do arquivo "Aluguel - Santos.ipynb".
