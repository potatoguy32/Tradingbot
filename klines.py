import CRUD
from datetime import datetime

def format_klines(klines: list, bot_id: int) -> None:
     for line in klines:
        line.pop(-1)
        line.insert(0, bot_id)

def initialize_klines(client, bot_id: int):
    klines_info = CRUD.get_klines_info(bot_id)
    klines = client.get_historical_klines(klines_info[0], klines_info[1], klines_info[2])
    format_klines(klines, bot_id)

    CRUD.push_klines(klines)
    print(f"{len(klines)} entries added")
    
def update_klines(client, bot_id: int):
    last_date = CRUD.get_last_date(bot_id)
    klines_info = CRUD.get_klines_info(bot_id)
    new_date = datetime.utcfromtimestamp((last_date + 1) / 1000).strftime("%d %b, %Y")
    klines = client.get_historical_klines(klines_info[0], klines_info[1], new_date)
    try:
        while klines[0][0] <= (last_date + 1):
            klines.pop(0)
            
        format_klines(klines, bot_id)

        CRUD.push_klines(klines)
        print(f"{len(klines)} entries added")
    
    except:
        print("Data is up to date")
        
        
