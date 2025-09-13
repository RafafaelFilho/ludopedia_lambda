from scrap.models.database import connect_database, download_games, register_data
from scrap.core.scraper import get_trs, parse_tr_to_auction

class SearchAuctions:
    def __init__(self, headers, batch_size, exclusive_key_start=None):
        self.headers=headers
        self.batch_size=batch_size
        self.engine=None
        self.games=[]
        self.new_auctions=[]
        self.has_more=None
        self.exclusive_key_start=exclusive_key_start

    def run(self):
        self.connect_to_db()
        self.load_games()
        self.scrape_auctions()
        self.save_new_auctions()

    def connect_to_db(self):
        self.engine=connect_database()

    def load_games(self):
        self.games, self.exclusive_key_start, self.has_more=download_games(self.engine, self.batch_size, self.exclusive_key_start)
        
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
            register_data(self.engine, self.new_auctions)
        
