from urllib.request import Request, urlopen, urlretrieve
from bs4 import BeautifulSoup
from urllib.error import URLError, HTTPError
import pandas as pd
#from IPython.core.display import display, HTML

def executar1(url):
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    #apenas exibe os valores das tags, sem busca
    print(soup.html)
    print(soup.html.head)
    print(soup.html.head.title)
    #exibe a 1 tag title que acha
    print(soup.title)
    #Exibir apenas o conteudo
    print(soup.title.get_text())

    # pegando a tag imagem
    retorno = soup.img.get('src')
    print(retorno)

    # find tag
    retorno = soup.find('h1').get_text()

    #find tag e id
    retorno = soup.find('h1', id='hello-world').get_text()
    print(retorno)

    retorno = soup.find('h1', {'class': 'sub-header'}).get_text()
    print(retorno)

    # findall
    #retorno = soup.findAll('src', limit=2)
    retorno = soup('img')#equivale ao findall

    retorno = soup.findAll(['h1','h2','h3'])#busca por lista
    print(retorno)

def executar2(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        retorno = soup.find('h1', id='hello-world').get_text()
        print(retorno)

    except HTTPError as e:
        print(e.status, e.reason)
    except URLError as e:
        print(e.reason)

def executar3(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        html = response.read()
        html = html.decode('utf-8')#para sites com caracteres como ç etc... resumindo converte para bytes string (type(html))
        html = " ".join(html.split()).replace('> <','><')# remove \t \n etc... depois remove o espaço entre tags

        print(html)

    except HTTPError as e:
        print(e.status, e.reason)
    except URLError as e:
        print(e.reason)

def executar4(url):
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    retorno = soup.findAll('p', {'class': 'txt-value'})#retorna uma lista
    print(retorno)

    retorno = soup.findAll('p', text='São Paulo - SP')  # retorna uma lista com tag p e que tenha algum texto sao paulo
    print(retorno)

    #alt é a tag, caso queira usar a tag class precisa class_='..' pois class é reservado pelo python
    retorno = soup.findAll('img', alt='Foto')
    for item in retorno:
        print(item.get('src'))

    retorno = soup.findAll(text=True)
    print(retorno)


def buscarValores(url):
    response = urlopen(url)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    cards = []
    card = {}

    #Pegar o anuncio
    anuncio = soup.find('div', {'class': 'well card'})
    card['value'] = anuncio.find('p', {'class': 'txt-value'}).getText()

    #pegar os detalhes
    infos = anuncio.find('div', {'class': 'body-card'}).findAll('p')
    for info in infos:
        card[info.get('class')[0].split('-')[-1]] = info.get_text()

    #pegar os acessorios
    items = anuncio.find('div', {'class': 'body-card'}).ul.findAll('li')
    items.pop()
    acessorios = []
    for item in items:
        acessorios.append(item.getText().replace('► ', ''))
    card['items'] = acessorios

    print(card)

    #Gerar o dataframe e salvar
    dataset = pd.DataFrame.from_dict(card, orient='index').T
    dataset.to_csv('data/dataset.csv', sep=';', index = False, encoding = 'utf-8-sig')

    #display(HTML("<img src=" + anuncio.find('div', {'class': 'image-card'}).img.get('src') + ">"))
    image = anuncio.find('div', {'class': 'image-card'}).img
    urlretrieve(image.get('src'), 'imagens/' + image.get('src').split('/')[-1])





if __name__ == '__main__':
    url = 'https://alura-site-scraping.herokuapp.com/'
    #url = input('Entre com a url: ')

    #executar1(url)
    #executar2(url)
    #executar3(url)
    #executar4(url)
    buscarValores(url)
