# %%

import requests

url = 'https://www.residentevildatabase.com/personagens/ada-wong/'

resp= requests.get(url)
# %%

resp.status_code
# %%

resp.text
# %%
from bs4 import BeautifulSoup

soup = BeautifulSoup(resp.text)

# %%
div_page = soup.find("div", class_ = "td-page-content")
paragrafo = div_page.find_all("p")[1]

# %%
ems = paragrafo.find_all("em")

# %%
ems[0].text

# %%
data = {}
for i in ems:
    chave, valor = i.text.split(":")
    chave = chave.strip(" ")
    data[chave] = valor.strip(" ")

data
# %%

# 50:32
# https://www.youtube.com/watch?v=K-bIZt_hSBo&list=PLvlkVRRKOYFSrkOL-Bze-42pTdJIAj0_h&index=3&t=669s&ab_channel=T%C3%A9oMeWhy