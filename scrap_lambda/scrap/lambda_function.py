from scrap.core.search_auctions import SearchAuctions
from scrap.core.update_auctions import UpdateAuctions
from scrap.utils.settings import settings
from logging import basicConfig
import logging
import json

def lambda_handler(event, context):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36'}
    basicConfig(
        level=logging.INFO,
        encondig='utf-8',
        format='%(levelname)s:%(asctime)s:%(message)s'
    )
    if settings.PROCESS=='searcher':
        key=event.get('secret_evaluated_key')
        key=event.get('batch')
        searcher=SearchAuctions(headers,key)
        searcher.run()
        logging.info(f'Leilões adicionados: {len(searcher.new_auctions)}')
        return {
            'statusCode': 200,
            'has_more': searcher.has_more,
            'secret_evaluated_key': searcher.exclusive_key_start
        }
    elif settings.PROCESS=='updater':
        updater=UpdateAuctions(headers)
        updater.run()
        return {
            'statusCode': 200,
            #'has_more': has_more,
            #'secret_evaluated_key': secret_evaluated_key
            'body': 'Processo no env é diferente'
        }
    else:
        return {
            'statusCode': 404,
            'body': 'Processo no env é diferente'
        }
    