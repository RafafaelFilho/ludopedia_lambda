from boto3.dynamodb.conditions  import Key
from scrap.utils.settings      import settings
import json
import boto3

def connect_database():
    dynamodb=boto3.resource('dynamodb',region_name='us-east-2')
    table=dynamodb.Table(settings.TABLE_NAME)
    return table

def download_active_auctions(table, batch_size, exclusive_key_start=None):        
    kwargs = {
        'IndexName': 'StatusIndex',
        'KeyConditionExpression': Key('status').eq('em andamento'),
        'Limit': batch_size
    }
    if exclusive_key_start:
        info_key={'ExclusiveStartKey':exclusive_key_start}
        kwargs.update(info_key)

    response = table.query(**kwargs)
    leiloes=response.get('Items')
    exclusive_key_start=response.get('LastEvaluatedKey')
    has_more=True if exclusive_key_start else False
    return leiloes, exclusive_key_start, has_more

def download_games(table, batch_size, exclusive_key_start=None):        
    kwargs = {
        'IndexName': 'TipoRegistroIndex',
        'KeyConditionExpression': Key('tipo_registro').eq('jogo'),
        'Limit': batch_size
    }
    if exclusive_key_start:
        info_key={'ExclusiveStartKey':exclusive_key_start}
        kwargs.update(info_key)

    response = table.query(**kwargs)
    jogos=response.get('Items')
    exclusive_key_start=response.get('LastEvaluatedKey')
    has_more=True if exclusive_key_start else False
    return jogos, exclusive_key_start, has_more

def auction_exists(table, pk, sk):
    response=table.get_item(
        Key={
            'PK':pk,
            'SK':sk
        }
    ).get('Item')
    if response:
        return True
    else:
        return False

def register_data(table, data_list):
    for data in data_list:
        table.put_item(Item=data)

def registry_update(table, update_info):
    for info in update_info:
        update_expressions = []
        expression_values = {}
        expression_names = {}

        for i, (campo, valor) in enumerate(info.items()):
            if campo!='PK' and campo!='SK':
                placeholder = f":val{i}"
                name_placeholder = f"#field{i}"
                update_expressions.append(f"{name_placeholder} = {placeholder}")
                
                expression_names[name_placeholder] = campo
                expression_values[placeholder] = valor

        response=table.update_item(
            Key={'PK': info['PK'], 'SK': info['SK']},
            UpdateExpression='SET ' + ', '.join(update_expressions),
            ExpressionAttributeValues=expression_values,
            ExpressionAttributeNames=expression_names
        )
    return response

def connect_s3():
    s3=boto3.resource('s3', region_name='us-east-2')
    return s3

def enviar_erro_s3(error_data):
    from datetime import datetime
    s3=connect_s3()
    file_path=f'erros/{error_data['type']}-error_type-{datetime.now().isoformat()}.txt'
    encoded_data=json.dumps(error_data,indent=3)
    obj=s3.Object(settings.BUCKET_ERROR_NAME, file_path)
    try:
        obj.put(Body=encoded_data.encode('utf-8'))
        return file_path
    except Exception as e:
        return e