from bs4                import BeautifulSoup
from scrap.core.scraper import get_trs, parse_tr_to_auction, get_updated_info
import responses

@responses.activate
def testar_pegar_os_trs_na_pagina_de_anuncios(game):
    with open(r'data\red_cathedral_pagina_anuncios_jogo.txt','r',encoding='utf-8') as f:
        html_mock=f.read()
    url_mock=f"https://ludopedia.com.br/jogo/{game.get('Item')['nome_ludopedia']}?v=anuncios"

    responses.add(
        responses.GET,
        url_mock,
        body=html_mock,
        status=200,
        content_type='text/html; charset=utf-8'
    )

    headers={'User-Agent':'test-agent'}
    trs=get_trs(game.get('Item'), headers)
    assert isinstance(trs, list)
    assert len(trs)>0

# fazer
#def testar_ERRO_pegar_os_trs_na_pagina_leilao_erro_sem_tr():
#def testar_ERRO_pegar_os_trs_na_pagina_leilao_erro_de_conexao():

def testar_transformacao_de_tr_para_dicionario(table_dynamodb_mock, game):
    with open(r'data\tr_leilao.txt','r',encoding='utf-8') as f:
        html_mock=f.read()
    tr=BeautifulSoup(html_mock, 'html.parser')
    response=parse_tr_to_auction(tr, game.get('Item'), table_dynamodb_mock)
    assert response['PK']==game.get('Item')['PK']
    assert response['link_leilao']!=None
    assert response['status']=='em andamento'

# fazer
#def testar_transformacao_de_tr_para_dicionario_mas_leilao_ja_existe(table_dynamo_mock, game, auction)
#def testar_transformacao_de_tr_para_dicionario_mas_tr_e_titulo()
#def testar_transformacao_de_tr_para_dicionario_mas_tr_e_anuncio()

def testar_buscar_informacoes_de_atualizacao_informacao_complementar(auction):
    with open(r'data\red_cathedral_pagina_leilao.txt','r',encoding='utf-8') as f:
        html_mock=f.read()
    url_mock=auction.get('Item')['link_leilao']
    responses.add(
        responses.GET,
        url_mock,
        body=html_mock,
        status=200,
        content_type='text/html; charset=utf-8'
    )
    headers={'User-Agent':'test-agent'}
    chaves=['observacoes', 'local', 'estado_item', 'data_alteracao']
    response=get_updated_info(auction.get('Item'), headers)

    assert isinstance(response,dict)
    assert all(chave in response for chave in chaves)

#def testar_buscar_informacoes_de_atualizacao_finalizacao
#def testar_buscar_informacoes_de_atualizacao_finalizacao_e_informacao_complementar
#def testar_buscar_informacoes_de_atualizacao_cancelado 