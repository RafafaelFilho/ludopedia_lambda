from scrap.core.update_auctions import UpdateAuctions
from utils.logger import logger_setup

if __name__ == '__main__':
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115 Safari/537.36'}
    logger_setup()
    UpdateAuctions(headers).run()
    
