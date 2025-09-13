from scrap.core.update_auctions import UpdateAuctions
from boto3.dynamodb.conditions import Key
from unittest.mock import patch
import responses

@responses.activate
def testar_updater_com_uma_pesquisa_que_vai_gerar_atualizacao(table_dynamodb_mock, game, auction):
    with patch('scrap.models.database.connect_database') as mock_connect:
        mock_connect.return_value=table_dynamodb_mock
        #mockando pagina de anuncions
        with open(r'data\red_cathedral_pagina_leilao.txt','r',encoding='utf-8') as f:
            html_mock=f.read()
        url_mock=f"https://ludopedia.com.br/leilao/627426/the-red-cathedral"
        responses.add(
            responses.GET,
            url_mock,
            body=html_mock,
            status=200,
            content_type='text/html; charset=utf-8'
        )

        headers={'User-Agent':'test-agent'}
        batch=20
        UpdateAuctions(headers, batch).run()

        response=table_dynamodb_mock.query(
            IndexName='TipoRegistroIndex',
            KeyConditionExpression=Key('tipo_registro').eq('leilao')
        )
        data=response.get('Items')
        #print(data)
        #assert len(data)==2
        #assert data[0]['PK']==data[1]['PK']
        #assert data[0]['SK']!=data[1]['SK']