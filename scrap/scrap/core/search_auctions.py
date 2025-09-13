import logging
from scrap.utils.logger import logger_setup
from scrap.models.database import connect_engine, download_games, add_auctions
from scrap.core.scraper import get_trs, parse_tr_to_auction

class SearchAuctions:
    def __inti__(self, headers):
        logger_setup()
        self.headers=headers
        self.engine=None
        self.games=[]
        self.new_auctions=[]

    def run(self):
        self.connect_to_db()
        self.load_games()
        self.scrape_auctions()
        self.save_new_auctions()
        logging.info(f'searchAuction: Process finished | {len(self.new_auctions)} auctions were added')

    def connect_to_db(self):
        self.engine=connect_engine('SearchAuction')

    def load_games(self):
        self.games=download_games(self.engine)

    def scrape_auctions(self):
        for game in self.games:
            trs=get_trs(game, self.headers)
            if not trs:
                continue
            for tr in trs:
                auction_data=parse_tr_to_auction(tr, game, self.engine)
                if auction_data:
                    self.new_auctions.append(auction_data)
                    
    def save_new_auctions(self):
        if self.new_auctions:
            add_auctions(self.new_auctions)
        
