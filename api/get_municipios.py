import requests
from DAO import *

def get_municipios():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter os municípios:", response.status_code)
        return []

municipios = get_municipios()

for municipio in municipios:
    sigla_estado = municipio['microrregiao']['mesorregiao']['UF']['sigla']
    nome_municipio = municipio['nome']
    insert_municipio(sigla_estado, nome_municipio)
    
