from scrap.models.database import connect_database, download_active_auctions, registry_update
from scrap.core.scraper import get_updated_info

class UpdateAuctions:
    def __init__(self, headers):
        self.headers=headers
        self.engine=None
        self.auctions=[]
        
    def run(self):
        self.connect_to_db()
        self.load_active_auctions()
        self.search_new_information()


    def connect_to_db(self):
        self.engine=connect_database()
    def load_active_auctions(self):
        self.auctions=download_active_auctions(self.engine)
    def search_new_information(self):
        for auction in self.auctions.get('Items'):
            print(auction)
            info=get_updated_info(auction, self.headers)
            if info:
                registry_update(self.engine, info, auction)
    
