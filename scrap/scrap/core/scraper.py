from bs4                    import BeautifulSoup
from datetime               import datetime, timedelta
from scrap.models.database  import auction_exists
import logging
import requests
import sys

def get_trs(game, headers)-> list:
    try:
        url = f'https://ludopedia.com.br/jogo/{game.nome_ludopedia}?v=anuncios'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')
        if trs:
            logging.debug('searchAuctions: TRs were found')
            return trs
        else:
            logging.error(
                'This page is differente', 
                exc_info=True, 
                extra={
                    'MainFunction':'searchAuctions',
                    'Function': 'findTrs',
                    'id':game.id,
                    'game_name': game.nome,
                    'soup': soup.find('body')
                }
            )
            return None
    except:
        logging.critical(
            'Connection error on Ludopedia',
            exc_info=True, 
            extra={
                'MainFunction':'searchAuctions',
                'Function': 'findTrs',
                'id':game.id,
                'game_name': game.nome
            }
        )
def parse_tr_to_auction(tr, game, engine) -> dict | None:
    a_tag = tr.find("a")
    if a_tag and a_tag.text.strip() == "Leilão":
        link = a_tag.get("href")
        auc_id = link.split("/")[4]
        if not auction_exists(engine, auc_id):
            now = datetime.now()# - timedelta(hours=3)
            return {
                "id_leilao": auc_id,
                "id_jogo": game.id,
                "link_leilao": link,
                "valor_pago": 0,
                "status": "em andamento",
                "data_alteracao": now,
                "data_registro": now
            }
        
def get_updated_info(auction, headers) -> dict | None:
    response = requests.get(auction.link_leilao, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    canceled_tag=soup.find('div', class_='alert alert-danger')
    if canceled_tag:
        if 'Para dar lances é necessário estar logado no site.' in canceled_tag.text or 'Leilão não encontrado ou excluído\n×\n' in canceled_tag.text:
            if 'Leilão não encontrado ou excluído\n×\n' in canceled_tag.text:
                info=canceled_info()
            else:
                complement_info=complement_info(auction, soup)
                finish_info=finish_info(auction, soup)
                info={**complement_info,**finish_info}
            logging.debug('UpdateAuction: Final data information created')
            return info
        else:
            logging.critical(
                'Canceled tag found but with different text', 
                extra={
                    'MainFunction':'UpdateAuctions',
                    'Function':'updateSelectionProcess',
                    'logging':'First Logging',
                    'id':auction.id,
                    'game_id': auction.id_jogo,
                    'auction_id': auction.id_leilao,
                    'link': auction.link_leilao,
                    'soup': soup.find('body')})
    else:
        logging.critical(
            'Somenthing happened that I dont know',
            extra={
                'MainFunction':'UpdateAuctions',
                'Function':'updateSelectionProcess',
                'logging':'Second Logging',
                'id':auction.id,
                'game_id': auction.id_jogo,
                'auction_id': auction.id_leilao,
                'link': auction.link_leilao,
                'soup': soup.find('body')
            }
        )
    return None



def canceled_info():
    logging.debug('UpdateAuction: Canceled info created')
    return {
        'status':'cancelado',
        'data_alteracao':datetime.now()#-timedelta(hours=3)
    }

def complement_info(auction, soup):
    try:
        if not auction.local:
            title=soup.find('h3',attrs=('class','title')).text.strip()
            desc=soup.find(id='bloco-descricao-item').text.strip()
            obs=f'{title}/|/|{desc}'
            local=soup.find_all('div',attrs=('class','media-body'))[3].text.split('(')[1].split(')')[0]
            estado_item = soup.find_all('div',attrs=('class','col-xs-12 col-md-6'))[3].text.split(':')[1].strip()
            info={
                'observacoes':obs,
                'local':local,
                'estado_item': 0 if estado_item=='Usado' else 1,
                'data_alteracao':datetime.now()-timedelta(hours=3)
            }
        else:
            info={}
        logging.debug('UpdateAuction: Complement info created')
        return info
    except:
        logging.error(
            'This page is differente', 
            exc_info=True, 
            extra={
                'MainFunction':'UpdateAuctions',
                'Function':'complementInfo',
                'id':auction.id,
                'game_id': auction.id_jogo,
                'auction_id': auction.id_leilao,
                'link': auction.link_leilao,
                'soup': soup.find('body')
            }
        )
        sys.exit()

def finish_info(auction, soup):
    try:
        spans=soup.find('div', class_='leilao-dados-lance form-group').find_all('span')
        value=spans[2].find('span') or spans[2].find('b')
        data_span=spans[0].find('span')
        if 'Finalizado' in data_span.text:
            end_date=datetime.strptime(data_span.text[12:-7] + '/2025', '%d/%m/%Y')
            try:
                value=int(value.text.replace("R$", "").replace(".", "").replace(",","").strip())
            except:
                value=0
            info={
                'valor_pago':value,
                'data_fim_leilao':end_date,
                'status':'finalizado',
                'data_alteracao':datetime.now()-timedelta(hours=3)
            }
        else:
            info={}
            
        logging.debug('UpdateAuction: Finish info created')
        return info
    except:
        logging.error(
            'This page is differente', 
            exc_info=True, 
            extra={
                'MainFunction':'UpdateAuctions',
                'Function':'finishInfo',
                'id':auction.id,
                'game_id': auction.id_jogo,
                'auction_id': auction.id_leilao,
                'link': auction.link_leilao,
                'soup': soup.find('body')
            }
        )
        sys.exit()