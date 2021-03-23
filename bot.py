import CRUD
import klines
from binance.client import Client

class Tradebot:
    def __init__(self, api_key: str, private_key: str, symbol: str, interval: str, start_date: str):
        self.api_key = api_key
        self.private_key = private_key
        self.symbol = symbol
        self.interval = interval
        self.start_date = start_date
        self.client = Client(self.api_key, self.private_key)
        CRUD.register(self.symbol, self.interval, self.start_date)
        self.id = CRUD.get_id(self.symbol, self.interval, self.start_date)
        self.client = Client(self.api_key, self.private_key)
        
    def update_klines(self):
        if not CRUD.exists_klines(self.id):
            klines.initialize_klines(self.client, self.id)
        
        else:
            klines.update_klines(self.client, self.id)