from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
import itertools 
from urllib.request import Request, urlopen
import requests
from requests import get
import time
from random import seed
from random import random
from random import randint
from unidecode import unidecode
import re


# specify the url format
url = 'https://www.vivareal.com.br/aluguel/sp/santos/apartamento_residencial/?__vt=ldph:a&pagina='
# initialize a list called houses 
houses = []
# initialize variable count at 1
count = 1

# first while loop that will run 100 times (adjust this to how many pages you want to scrape)
while count <= 235:
    # initialize variable new_count at 0
    new_count = 0

    # if loop that specifies the first page separately (many websites have a first page url format different than other pages)
    if count == 1:
        first_page = 'https://www.vivareal.com.br/aluguel/sp/santos/apartamento_residencial/?__vt=ldph:a&pagina=1'
        session = HTMLSession()
        r = session.get(first_page, headers={'User-Agent': 'Mozilla/5.0'})
        r.html.render()
        # parse through the html 
        html_soup = BeautifulSoup(r.html.html, 'html.parser')
        house_data = html_soup.find_all('div', class_="property-card__main-content")
        print(first_page)
    
        # if the response was not empty (if something was actually scraped)
        if house_data != []:
            # add to the list houses
            houses.extend(house_data)

    # pages other than the first
    elif count != 1:

    # collect four and wait random times 
        url = 'https://www.vivareal.com.br/aluguel/sp/santos/apartamento_residencial/?__vt=ldph:a&pagina=' + str(count)
        session = HTMLSession()
        r = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        r.html.render(sleep = 10)
        # parse through the html 
        html_soup = BeautifulSoup(r.html.html, 'html.parser')
        house_data = html_soup.find_all('div', class_="property-card__main-content")
        print(url)

        if house_data != []:
            houses.extend(house_data)

        #if you get empty response, stop the loop
        else:
            print('empty')
            break

    count += 1

## DATA FORMATTING 
## initializing lists and variables
count = 0
house_price = []
location = []
city = []
bedrooms = []
bathrooms = []
parking = []
surface = []
## how long we are running the while loop for 
n = int(len(houses)) - 1

while count <= n:
    # running the loop through each html bin we scraped
    num = houses[int(count)]
    
    # getting the price: make sure to test this code a few times by itself to understand exactly which parameters will work 
    price = num.find_all('div',{"class":"property-card__price js-property-card-prices js-property-card__price-small"})[0].text    
    house_price.append(price)
    df_price = pd.DataFrame({'rent':house_price})
    df_price['rent'] = df_price['rent'].str.replace("\D","")
    df_price['rent'] = df_price['rent'].str.replace("/mês","")   
    
   #getting the postcode: make sure to test this code a few times by itself to understand exactly which parameters will work 
    postcode = num.find('span',{"class":"property-card__address"}).text
    location.append(postcode)
    df_postcode = pd.DataFrame({'endereco':location})
    df_postcode['endereco'] = df_postcode['endereco'].apply(lambda x: x.split('-')[0])
    #df_postcode['endereco'] = df_postcode['endereco'].apply(lambda x: re.sub("\d+", "", x))
    #df_postcode['endereco'] = df_postcode['endereco'].apply(lambda x: x.replace(',',''))
    df_postcode['endereco'] = df_postcode['endereco'].apply(lambda x: x.replace('\n',''))
    
    
    #getting the number of bedrooms: make sure to test this code a few times by itself to understand exactly which parameters will work 
    bedrooms_num = num.find_all('li',{"class":"property-card__detail-item property-card__detail-room js-property-detail-rooms"})[0].text
    bedrooms.append(bedrooms_num)
    df_bedrooms = pd.DataFrame({'rooms':bedrooms})
    df_bedrooms['rooms'] = df_bedrooms['rooms'].str.replace("\D","")
    
    #getting the number of bathrooms: make sure to test this code a few times by itself to understand exactly which parameters will work 
    bathrooms_num = num.find_all('li',{"class":"property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom"})[0].text
    bathrooms.append(bathrooms_num)
    df_bathrooms = pd.DataFrame({'bathroom':bathrooms})
    df_bathrooms['bathroom'] = df_bathrooms['bathroom'].str.replace("\D","")

    #getting the number of parking spaces: make sure to test this code a few times by itself to understand exactly which parameters will work 
    parking_num = num.find_all('li',{"class":"property-card__detail-item property-card__detail-room js-property-detail-rooms"})[0].text
    parking.append(parking_num)
    df_parking = pd.DataFrame({'parking':parking})
    df_parking['parking'] = df_parking['parking'].str.replace("\D","")

    
    #getting the sq meter size: make sure to test this code a few times by itself to understand exactly which parameters will work 
    size = num.find_all('span',{"class":"property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area"})[0].text
    surface.append(size)
    df_surface = pd.DataFrame({'area':surface})
    df_surface['area'] = df_surface['area'].str.replace("\D","")
    
    print(count)
    
    count += 1

# concat all the different dataframes created, culminating in dfa (completed dataframe)
result = pd.concat([df_price, df_postcode], axis=1, sort=False)
result2 = pd.concat([result, df_bedrooms], axis=1, sort=False)
result3 = pd.concat([result2, df_bathrooms], axis=1, sort=False)
result4 = pd.concat([result3, df_parking], axis=1, sort=False)
dfa = pd.concat([result4, df_surface], axis=1, sort=False)

dfa['endereco'] = dfa['endereco'].apply(lambda x: x.split('-')[0])
dfa['endereco'] = dfa['endereco'].apply(lambda x: re.sub("\d+", "", x))
dfa['endereco'] = dfa['endereco'].apply(lambda x: x.replace(',',''))

dfa.to_csv('santos_rent.csv')