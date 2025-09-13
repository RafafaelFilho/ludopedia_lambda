from scrap.core.scraper import get_trs, parse_tr_to_auction
import responses
from bs4 import BeautifulSoup

@responses.activate
def testar_pegar_os_trs_na_pagina_de_anuncios(game):
    with open('data/red_cathedral_pagina_anuncios_jogo','r',encoding='utf-8') as f:
        html_mock=f.read()
    url_mock=f'https://ludopedia.com.br/jogo/{game.nome_ludopedia}?v=anuncios'

    responses.add(
        responses.GET,
        url_mock,
        body=html_mock,
        status=200,
        content_type='text/html; charset=utf-8'
    )

    headers={'User-Agent':'test-agent'}
    trs=get_trs(game, headers)

    assert isinstance(trs, list)
    assert len(trs)>0

def testar_transformacao_de_tr_para_dicionario(game):
    with open('data/pagina_anuncios_jogo.txt','r',encoding='utf-8') as f:
        html_mock=f.read()
    url_mock=f'https://ludopedia.com.br/jogo/{game.nome_ludopedia}?v=anuncios'
    



