from scrap.models.database import download_active_auctions, download_games, register_data, registry_update, auction_exists, enviar_erro_s3
from tests.conftest import download_auction
from scrap.utils.settings import settings
from unittest.mock import patch
import json

def testar_leitura_leiloes(table_dynamodb_mock, auction):
    response, chave, has_more=download_active_auctions(table_dynamodb_mock,20)
    assert has_more==False
    assert chave==None
    assert len(response)==1

def testar_leitura_jogos_sem_outra_volta(table_dynamodb_mock, game):
    response, chave, has_more=download_games(table_dynamodb_mock, 1)
    assert has_more==False
    assert chave==None
    assert len(response)==1
    
def testar_leitura_jogos_com_outra_volta(table_dynamodb_mock, game, game2):
    response, chave, has_more=download_games(table_dynamodb_mock, 1)
    assert has_more==True
    assert chave!=None
    assert len(response)==1

def testar_adicionar_leilao(table_dynamodb_mock, game):
    data=[
        {
            'PK': game.get('Item')['PK'], 'SK': 'LEILAO#456', 'tipo_registro':'leilao', 'id_leilao': 456, 
            'link_leilao': 'https://example.com','valor_pago': None, 'data_fim_leilao': '2025-09-01T00:00:00Z', 
            'status': 'em andamento', 'observacoes': 'Otimo estado', 'data_alteracao': '2025-09-01T00:00:00Z', 
            'local': None, 'estado_item': None, 'data_registro': '2025-09-01T00:00:00Z'
        }
    ]
    register_data(table_dynamodb_mock, data)
    response=download_auction(table_dynamodb_mock, data[0]['PK'], data[0]['SK'])
    assert response.get('ResponseMetadata')['HTTPStatusCode']==200
    assert response.get('Item')['PK']==data[0]['PK']
    assert response.get('Item')['SK']==data[0]['SK']

def testar_existencia_de_leilao(table_dynamodb_mock,auction):
    response=auction_exists(table_dynamodb_mock, auction.get("Item")['PK'], auction.get("Item")['SK'])
    assert response==True

def testar_nao_existencia_de_leilao(table_dynamodb_mock):
    import uuid
    response=auction_exists(table_dynamodb_mock, uuid.uuid4().bytes, '123')
    assert response==False






def testar_atualizar_leilao_sem_finalizacao(table_dynamodb_mock, auction):
    update_info=[
        {
            'PK':auction.get('Item')['PK'],
            'SK':auction.get('Item')['SK'],
            'observacoes': 'Sem detalhes', 
            'local': 'Niterói - RJ',
            'estado_item': True
        }
    ]
    registry_update(table_dynamodb_mock, update_info)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': auction.get('Item')['PK'],
            'SK': auction.get('Item')['SK']
        }
    )
    assert response.get('Item')['PK'] == auction.get('Item')['PK']
    assert response.get('Item')['SK'] == auction.get('Item')['SK']
    assert response.get('Item')['observacoes'] != auction.get('Item')['observacoes']
    assert response.get('Item')['local'] != auction.get('Item')['local']
    assert response.get('Item')['estado_item'] != auction.get('Item')['estado_item']

def testar_atualizar_leilao_só_finalizacao(table_dynamodb_mock, auction):
    update_info=[
        {
            'PK':auction.get('Item')['PK'],
            'SK':auction.get('Item')['SK'],
            'valor_pago': 17000,
            'status': 'finalizado'
        }
    ]
    registry_update(table_dynamodb_mock, update_info)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': auction.get('Item')['PK'],
            'SK': auction.get('Item')['SK']
        }
    )
    assert response.get('Item')['PK'] == auction.get('Item')['PK']
    assert response.get('Item')['SK'] == auction.get('Item')['SK']
    assert response.get('Item')['valor_pago'] != auction.get('Item')['valor_pago']
    assert response.get('Item')['status'] != auction.get('Item')['status']

def testar_atualizar_leilao_com_finalizacao(table_dynamodb_mock, auction):
    update_info=[
        {
            'PK':auction.get('Item')['PK'],
            'SK':auction.get('Item')['SK'],
            'valor_pago': 17000, 
            'observacoes': 'Sem detalhes', 
            'local': 'Niterói - RJ',
            'estado_item': True,
            'valor_pago': 17000,
            'status': 'finalizado'
        }
    ]
    registry_update(table_dynamodb_mock, update_info)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': auction.get('Item')['PK'],
            'SK': auction.get('Item')['SK']
        }
    )
    assert response.get('Item')['PK'] == auction.get('Item')['PK']
    assert response.get('Item')['SK'] == auction.get('Item')['SK']
    assert response.get('Item')['valor_pago'] != auction.get('Item')['valor_pago']
    assert response.get('Item')['observacoes'] != auction.get('Item')['observacoes']
    assert response.get('Item')['local'] != auction.get('Item')['local']
    assert response.get('Item')['estado_item'] != auction.get('Item')['estado_item']
    assert response.get('Item')['valor_pago'] != auction.get('Item')['valor_pago']
    assert response.get('Item')['status'] != auction.get('Item')['status']

def test_envio_arquivo_s3(s3_mock):
    with patch('scrap.models.database.connect_s3') as mock_connect:
        mock_connect.return_value=s3_mock
        error_data={
            'type':'CRITICAL',
            'function':'complement_info',
            'body':'<body></body>'
        }
        file_path=enviar_erro_s3(error_data)
        file=s3_mock.Object(settings.BUCKET_ERROR_NAME, file_path)
        response=file.get()
        undecoded_data = response['Body'].read()
        data_str = undecoded_data.decode('utf-8')
        data = json.loads(data_str)
        
        assert data['type'] == error_data['type']
        assert data['function'] == error_data['function']
        assert data['body'] == error_data['body']
