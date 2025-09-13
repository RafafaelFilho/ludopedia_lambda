from scrap.core.search_auctions import SearchAuctions
from boto3.dynamodb.conditions  import Key
from unittest.mock import patch
import responses

@responses.activate
def testar_ERRO_searcher_com_uma_pesquisa_que_vai_gerar_dois_registros_de_leilao(table_dynamodb_mock, game):
    # mockando aws
    with patch('scrap.models.database.connect_database') as mock_connect:
        mock_connect.return_value=table_dynamodb_mock
        #mockando pagina de anuncions
        with open(r'data\red_cathedral_pagina_anuncios_jogo.txt','r',encoding='utf-8') as f:
            html_mock=f.read()
        url_mock=f"https://ludopedia.com.br/jogo/the-red-cathedral?v=anuncios"
        responses.add(
            responses.GET,
            url_mock,
            body=html_mock,
            status=200,
            content_type='text/html; charset=utf-8'
        )

        headers={'User-Agent':'test-agent'}
        batch=20
        searcher=SearchAuctions(headers, batch)
        searcher.run()

        response=table_dynamodb_mock.query(
            IndexName='TipoRegistroIndex',
            KeyConditionExpression=Key('tipo_registro').eq('leilao')
        )
        data=response.get('Items')
        assert len(data)==2
        assert data[0]['PK']==data[1]['PK']
        assert data[0]['SK']!=data[1]['SK']

@responses.activate
def testar_ERRO_searcher_com_uma_pesquisa_que_vai_gerar_um_registro_de_leilao(table_dynamodb_mock, game, auction2):
    # mockando aws
    with patch('scrap.models.database.connect_database') as mock_connect:
        mock_connect.return_value=table_dynamodb_mock
        #mockando pagina de anuncions
        with open(r'data\red_cathedral_pagina_anuncios_jogo.txt','r',encoding='utf-8') as f:
            html_mock=f.read()
        url_mock=f"https://ludopedia.com.br/jogo/the-red-cathedral?v=anuncios"
        responses.add(
            responses.GET,
            url_mock,
            body=html_mock,
            status=200,
            content_type='text/html; charset=utf-8'
        )

        response=table_dynamodb_mock.query(
            IndexName='TipoRegistroIndex',
            KeyConditionExpression=Key('tipo_registro').eq('leilao')
        )
        data_antes=response.get('Items')

        headers={'User-Agent':'test-agent'}
        batch=20
        searcher=SearchAuctions(headers, batch)
        searcher.run()

        response=table_dynamodb_mock.query(
            IndexName='TipoRegistroIndex',
            KeyConditionExpression=Key('tipo_registro').eq('leilao')
        )
        data=response.get('Items')
        assert len(data_antes)==1
        assert len(data)==2
        assert data[0]['PK']==data[1]['PK']
        assert data[0]['SK']!=data[1]['SK']