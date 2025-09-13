from bs4                    import BeautifulSoup
from datetime               import datetime, timedelta
from scrap.models.database  import auction_exists, enviar_erro_s3
import logging
import requests

def get_trs(game, headers)-> list:
    try:
        url = f"https://ludopedia.com.br/jogo/{game['nome_ludopedia']}?v=anuncios"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        trs = soup.find_all('tr')
        if trs:
            return trs
        else:
            error={
                'type':'CRITICAL',
                'function':'get_trs',
                'id':game['id'],
                'game_name':game['name'],
                'body':soup.find('body')
            }
            file_path=enviar_erro_s3(error)
            logging.critical(f"Erro: Nenhum <tr>, Arquivo gerado: {file_path}")
            return None
    except Exception as e:
        logging.error(f'Erro: Não conseguiu conectar com o servidor, ERRO: {e}')
        return None

def parse_tr_to_auction(tr, game, engine) -> dict | None:
    a_tag = tr.find("a")
    if a_tag and a_tag.text.strip() == "Leilão":
        link = a_tag.get("href")
        auc_id = link.split("/")[4]
        sk='LEILAO#'+auc_id
        conf=auction_exists(engine, game['PK'], sk)
        if not conf:
            now = datetime.now() - timedelta(hours=3)
            return {
                'PK':game['PK'],
                'SK':'LEILAO#' + str(auc_id),
                "id_leilao": auc_id,
                "link_leilao": link,
                "valor_pago": 0,
                "status": "em andamento",
                "data_alteracao": str(now),
                "data_registro": str(now),
                'tipo_registro':'leilao'
            }
        return None
        
def get_updated_info(auction, headers) -> dict | None:
    response = requests.get(auction['link_leilao'], headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    canceled_tag=soup.find('div', class_='alert alert-danger')
    if canceled_tag:
        if 'Para dar lances é necessário estar logado no site.' in canceled_tag.text:
            c_info=complement_info(auction, soup)
            f_info=finish_info(auction, soup)
            info={**c_info,**f_info}
            return info
        elif 'Leilão não encontrado ou excluído\n×\n' in canceled_tag.text:
            info=canceled_info()
            return info
        else:
            error={
                'type':'CRITICAL',
                'function':'get_updated_info',
                'PK':auction['PK'],
                'SK':auction['SK'],
                'body':soup.find('body')
            }
            file_path=enviar_erro_s3(error)
            logging.critical(f"Erro: 'canceled_tag' foi encontrada mas com texto diferente, Arquivo gerado: {file_path}")
    else:
        error={
            'type':'CRITICAL',
            'function':'get_updated_info',
            'PK':auction['PK'],
            'SK':auction['SK'],
            'body':soup.find('body')
        }
        file_path=enviar_erro_s3(error)
        logging.critical(f"Erro: Não achou 'canceled_tag', Arquivo gerado: {file_path}")
    return None



def canceled_info():
    return {

        'status':'cancelado',
        'data_alteracao':str(datetime.now()-timedelta(hours=3))
    }

def complement_info(auction, soup):
    try:
        if not auction['local']:
            title=soup.find('h3',attrs=('class','title')).text.strip()
            desc=soup.find(id='bloco-descricao-item').text.strip()
            obs=f'{title}/|/|{desc}'
            local=soup.find_all('div',attrs=('class','media-body'))[3].text.split('(')[1].split(')')[0]
            estado_item = soup.find_all('div',attrs=('class','col-xs-12 col-md-6'))[3].text.split(':')[1].strip()
            info={
                'PK':auction['PK'],
                'SK':auction['SK'],
                'observacoes':obs,
                'local':local,
                'estado_item': 0 if estado_item=='Usado' else 1,
                'data_alteracao': str(datetime.now()-timedelta(hours=3))
            }
        else:
            info={}
        return info
    except Exception as e:
        error={
            'type':'CRITICAL',
            'function':'complement_info',
            'PK':auction['PK'],
            'SK':auction['SK'],
            'body':soup.find('body')
        }
        file_path=enviar_erro_s3(error)
        logging.critical(f"Erro: A pagina esta diferente, Arquivo gerado: {file_path}, ERRO: {e}")

def finish_info(auction, soup):
    try:
        spans=soup.find('div', class_='leilao-dados-lance form-group').find_all('span')
        value=spans[2].find('span') or spans[2].find('b')
        data_span=spans[0].find('span')
        if 'Finalizado' in data_span.text:
            end_date=str(datetime.strptime(data_span.text[12:-7] + '/2025', '%d/%m/%Y'))
            try:
                value=int(value.text.replace("R$", "").replace(".", "").replace(",","").strip())
            except:
                value=0
            info={
                'valor_pago':value,
                'data_fim_leilao':end_date,
                'status':'finalizado',
                'data_alteracao':str(datetime.now()-timedelta(hours=3))
            }
        else:
            info={}
        return info
    except Exception as e:
        error={
            'type':'CRITICAL',
            'function':'finish_info',
            'PK':auction['PK'],
            'SK':auction['SK'],
            'body':soup.find('body')
        }
        file_path=enviar_erro_s3(error)
        logging.critical(f"Erro: Algum erro na coleta de informações para a finalização: {file_path}, ERRO: {e}")