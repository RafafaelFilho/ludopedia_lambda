from scrap.models.database import connect_database, download_active_auctions, registry_update
from scrap.core.scraper import get_updated_info

class UpdateAuctions:
    def __init__(self, headers, batch_size, exclusive_key_start=None):
        self.headers=headers
        self.batch_size=batch_size
        self.engine=None
        self.auctions=[]
        self.update_info=[]
        self.has_more=None
        self.exclusive_key_start=exclusive_key_start
        
    def run(self):
        self.connect_to_db()
        self.load_active_auctions()
        self.search_new_information()
        self.update_auctions()

    def connect_to_db(self):
        self.engine=connect_database()

    def load_active_auctions(self):
        self.auctions, self.exclusive_key_start, self.has_more=download_active_auctions(self.engine, self.batch_size, self.exclusive_key_start)

    def search_new_information(self):
        for auction in self.auctions:
            info=get_updated_info(auction, self.headers)
            if info:
                self.update_info.append(info)

    def update_auctions(self):
        registry_update(self.engine, self.update_info)