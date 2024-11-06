import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd


def ScrapPubMed(keyword:str):
  link = f'https://pubmed.ncbi.nlm.nih.gov/?term={keyword.lower()}&filter=datesearch.y_1'

  #Fiz a requisição
  req = requests.get(link)

  #Jogar o HTML Bruto
  soup = BeautifulSoup(req.text, 'html.parser')

  soup = soup.find_all('article', attrs={'class':'full-docsum'})

  #Pega a data e link da noticia
  soup = [divs.find('div', attrs={"class":'docsum-wrap'}) for divs in soup]

  noticeName = []
  noticeLink = []
  noticeDataRef = []

  for infos in soup:
    #Pegar link das noticias
    docontent = infos.find('div', class_='docsum-content')
    noticiaCode = docontent.find('a', class_='docsum-title')
    Code = noticiaCode['href'] if noticiaCode else None
    noticiaLink = 'https://pubmed.ncbi.nlm.nih.gov'+Code
    noticeLink.append(noticiaLink)

    #Pegar nome da noticia
    name = noticiaCode.text.strip()
    noticeName.append(name)
    data_ref = docontent.find('div',class_='docsum-citation full-citation').find('span',class_='docsum-journal-citation full-journal-citation').text
    noticeDataRef.append(data_ref)

  df = {'NoticeName':noticeName,'NoticeLink':noticeLink,'DataRef':noticeDataRef}
  df = pd.DataFrame(df)

  return df

# Configuração inicial da pagina
st.set_page_config(page_title='Scrapping', layout='wide')

# Menu de navegação
st.sidebar.header('Navegação')
page = st.sidebar.radio("Selecione uma página", ('PubMed', 'Scielo'))

if page == 'PubMed':
  st.header('Scrapping da Página PubMed')

  with st.form(key='scrapping'):
    keyword = st.text_input('Palavra-Chave')

    submit_button = st.form_submit_button(label='Buscar') 

    if submit_button:
      df = ScrapPubMed(keyword)

      st.header('Consulta do PubMed')   
      st.dataframe(df)

if page == 'Scielo':
  st.header('Scrapping da Página Scielo')

  with st.form(key='scrapping'):
    keyword = st.text_input('Palavra-Chave')

    submit_button = st.form_submit_button(label='Buscar') 

    if submit_button:
      df_2 = pd.read_excel('medicamentos.xlsx')

      st.header('Consulta do Scielo')   
      st.dataframe(df_2)

    

      

