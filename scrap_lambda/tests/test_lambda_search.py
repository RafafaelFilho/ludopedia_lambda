from scrap.lambda_function import lambda_handler
from scrap.models.database import download_games
from unittest.mock import patch
import responses
import os

@patch.dict(os.environ, {'PROCESS':'searcher'})
def testar_a_funcao_principal_como_searcher(table_dynamodb_mock, game, game2):
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
        with open(r'data\arcs_pagina_anuncios_jogo.txt','r',encoding='utf-8') as f:
            html_mock=f.read()
        url_mock=f"https://ludopedia.com.br/jogo/arcs?v=anuncios"
        responses.add(
            responses.GET,
            url_mock,
            body=html_mock,
            status=200,
            content_type='text/html; charset=utf-8'
        )
        fake_event={
            'batch':20
        }
        fake_context=1

        while True:
            response=lambda_handler(fake_event, fake_context)
            if response.get('has_more'):
                fake_event={
                    'has_more': True,
                    'secret_evaluated_key': response.get('secret_evaluated_key')
                }
            else:
                break
    assert response['statusCode']==200
    assert response['has_more']==False
    assert response['secret_evaluated_key']==None
            