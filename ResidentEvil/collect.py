# %%

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

# %%
def get_content(url):
    resp= requests.get(url)
    return resp

def get_basic_infos(soup):
    div_page = soup.find("div", class_ = "td-page-content")
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    data = {}
    for i in ems:
        chave, valor = i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    return data

def get_aparicoes(soup):
    lis = (soup.find("div", class_ = "td-page-content")
                .find("h4")
                .find_next()
                .find_all("li"))
    
    aparicoes = [i.text for i in lis]
    return aparicoes

def get_personagem_infos(url):
    resp = get_content(url)
    if resp.status_code != 200:
        print('Não foi possível obter os dados')
        return {}
    else:
        soup = BeautifulSoup(resp.text)
        data = get_basic_infos(soup)
        data["Aparicoes"] = get_aparicoes(soup)
        return data

def get_links():
    url = 'https://www.residentevildatabase.com/personagens/ada-wong/'
    resp = requests.get(url)
    soup_personagens = BeautifulSoup(resp.text)
    ancoras = (soup_personagens.find("div", class="td-page-content")
                                .find_all("a"))
    
    links = [i["href"] for i in ancoras]

    return links

# %%
links = get_links()
data = []
for i in tqdm(links):
    d = get_personagem_infos(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-"," ").title()
    d["Nome"] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df.to_parquet("dados_re.parquet", index=False)
df.to_pickle("dados.re_pkl")
