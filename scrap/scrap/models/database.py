from sqlmodel import create_engine, Session, text, select
from scrap.config.settings import settings
from scrap.models.entities import Jogo, Leilao
import logging
import sys

def connect_engine(process):
    try:
        engine=create_engine(settings.database_url)
        with Session(engine) as session:
            session.exec(text('SELECT 1'))
            logging.debug('Database connected')
        return engine
    except:
        logging.error(f'{process}: Database connection failed', exc_info=True)
        sys.exit()

def download_games(engine):
    try:
        with Session(engine) as session:
            games=session.exec(select(Jogo)).all()
        logging.debug('SearchAuctions: Games were downloaded')
        return games
    except:
        logging.critical(
            'Download error', 
            exc_info=True, 
            extra={
                'MainFunction':'SearchAuctions',
                'Function':'download_games'
            }
        )

def auction_exists(engine, auc_id):
    with Session(engine) as session:
        query=session.exec(select(Leilao).where(Leilao.id_leilao==auc_id)).first()
        if query:
            logging.debug('SearchAuction: Auction already exists in the database')
            return True
        else:
            logging.debug("SearchAuction: Auction doesn't exist in the database")
            return False

def add_auctions(engine, auctions: list):
    try:
        with Session(engine) as session:
            for auction in auctions:
                l=Leilao(**auction)
                session.add(l)
            session.commit()
        logging.debug('SearchAuction: Auctions have been added')
    except:
        logging.critical('Error to add new auctions',
            exc_info=True, 
            extra={
                'MainFunction':'SearchAuctions',
                'Function': 'add_auction'
            }
        )
        sys.exit()

def download_active_auctions(engine):
    try:
        with Session(engine) as session:
            auctions=session.exec(select(Leilao).where(Leilao.status=='em andamento')).all()
        logging.debug('UpdateAuctions: Auctions downloaded')
        return auctions
    except:
        logging.critical(
            'Error to download', 
            exc_info=True, 
            extra={
                'MainFunction':'UpdateAuctions',
                'Function':'downloadAuctions' 
            }
        ) 

def save_updates(engine, auction, info):
    with Session(engine) as session:
        for key, value in info.items():
            setattr(auction,key,value)
        session.add(auction)
        session.commit()
