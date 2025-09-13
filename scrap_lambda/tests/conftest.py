import boto3
from moto import mock_aws
from pytest import fixture
from scrap.utils.settings import settings
from boto3.dynamodb.conditions import Key
import uuid

@fixture
def common_pk():
    return uuid.uuid4().bytes

@fixture
def s3_mock():
    with mock_aws():
        s3=boto3.resource('s3', region_name='us-east-2')
        s3.create_bucket(
            Bucket=settings.BUCKET_ERROR_NAME,
            CreateBucketConfiguration={'LocationConstraint': 'us-east-2'}
        )
        yield s3


@fixture
def table_dynamodb_mock():
    with mock_aws():
        dynamodb=boto3.resource('dynamodb', region_name='us-east-2')
        table=create_table(dynamodb)
        table.meta.client.get_waiter('table_exists').wait(TableName=settings.TABLE_NAME)
        yield table

@fixture
def game(table_dynamodb_mock, common_pk):
    data={
        'PK':common_pk, 'SK':'METADATA', 'tipo_registro':'jogo', 'nome':'The Red Cathedral','nome_ludopedia':'the-red-cathedral'
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response

@fixture
def game2(table_dynamodb_mock):
    data={
        'PK':uuid.uuid4().bytes, 'SK':'METADATA', 'tipo_registro':'jogo', 'nome':'ARCS','nome_ludopedia':'arcs'
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response

@fixture
def game3(table_dynamodb_mock):
    data={
        'PK':uuid.uuid4().bytes, 'SK':'METADATA', 'tipo_registro':'jogo', 'nome':'Assyria','nome_ludopedia':'assyria'
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response

@fixture
def auction(table_dynamodb_mock, common_pk):
    data={
        'PK': common_pk, 'SK': 'LEILAO#627426', 'tipo_registro':'leilao', "id_leilao": 627426, 
        "link_leilao": "https://ludopedia.com.br/leilao/627426/the-red-cathedral",
        "valor_pago": None, "data_fim_leilao": None, "status": "em andamento",
        "observacoes": None, "data_alteracao": "2025-09-01T00:00:00Z", 
        "local": None, "estado_item": None, "data_registro": "2025-09-01T00:00:00Z"
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response

@fixture
def auction2(table_dynamodb_mock, common_pk):
    data={'PK': common_pk, 'SK': 'LEILAO#627426', 'id_leilao': '627426', 
        'link_leilao': 'https://ludopedia.com.br/leilao/627426/the-red-cathedral', 
        'valor_pago': 0, 'status': 'em andamento', 'data_alteracao': '2025-09-03 22:14:43.228097', 
        'data_registro': '2025-09-03 22:14:43.228097', 'tipo_registro': 'leilao'
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response
@fixture
def auction3(table_dynamodb_mock, common_pk):
    data={'PK': common_pk, 'SK': 'LEILAO#627426', 'id_leilao': '627426', 
        'link_leilao': 'https://ludopedia.com.br/leilao/632030/arcs', 
        'valor_pago': 0, 'status': 'em andamento', 'data_alteracao': '2025-09-03 22:14:43.228097', 
        'data_registro': '2025-09-03 22:14:43.228097', 'tipo_registro': 'leilao'
    }
    table_dynamodb_mock.put_item(Item=data)
    response=table_dynamodb_mock.get_item(
        Key={
            'PK': data['PK'],
            'SK': data['SK'],
        }
    )
    return response

def create_table(dynamodb):
    attr_def=[
        {'AttributeName':'PK','AttributeType':'B'},
        {'AttributeName':'SK','AttributeType':'S'},
        {'AttributeName':'tipo_registro', 'AttributeType':'S'},
        {'AttributeName': 'nome_ludopedia', 'AttributeType': 'S'},
        {'AttributeName': 'status', 'AttributeType': 'S'}
    ]
    key_schema=[
        {'AttributeName':'PK','KeyType':'HASH'},
        {'AttributeName':'SK','KeyType':'RANGE'}
    ]
    table=dynamodb.create_table(
        TableName=settings.TABLE_NAME,
        AttributeDefinitions=attr_def,
        KeySchema=key_schema,
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        },
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'TipoRegistroIndex',
                'KeySchema': [
                    {'AttributeName': 'tipo_registro', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'NomeLudopediaIndex',
                'KeySchema': [
                    {'AttributeName': 'nome_ludopedia', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            },
            {
                'IndexName': 'StatusIndex',
                'KeySchema': [
                    {'AttributeName': 'status', 'KeyType': 'HASH'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        ]
    )
    return table

def download_auction(table, pk, sk):
    response=table.get_item(
        Key={
            'PK':pk,
            'SK':sk
        }
    )
    return response