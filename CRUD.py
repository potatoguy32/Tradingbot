import psycopg2


conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
cur = conn.cursor()
cur.execute("""
            CREATE TABLE IF NOT EXISTS bots(
                id serial PRIMARY KEY,
                symbol varchar(12) NOT NULL,
                interval varchar(8) NOT NULL,
                start_date varchar(24) NOT NULL);""")
conn.commit()
cur.execute("""
            CREATE TABLE IF NOT EXISTS klines(
                id serial PRIMARY KEY,
                bot_id integer NOT NULL,
                open_time bigint NOT NULL,
                open_value double precision NOT NULL,
                high double precision NOT NULL,
                low double precision NOT NULL,
                close_value double precision NOT NULL,
                volume double precision NOT NULL,
                close_time bigint NOT NULL,
                quote_asset_volume double precision NOT NULL,
                trades_number integer NOT NULL,
                taker_buy_base double precision NOT NULL,
                taker_buy_quote double precision NOT NULL);""")
conn.commit()
cur.execute("""
            CREATE TABLE IF NOT EXISTS orders(
                id serial PRIMARY KEY,
                bot_id integer NOT NULL,
                time bigint NOT NULL,
                transaction varchar(8) NOT NULL,
                price double precision NOT NULL,
                status varchar(16) NOT NULL);""")
conn.commit()  
conn.close()
                        
def register(symbol: str, interval: str, start_date: str) -> None:
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.execute("SELECT * FROM bots WHERE symbol = %s AND interval = %s AND start_date = %s;",
                    (symbol, interval, start_date))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO bots (symbol, interval,  start_date) VALUES (%s, %s, %s);",
                        (symbol, interval, start_date))
            conn.commit()
    
    except:
        print("Error while registering")
            
    finally:
        if conn:
            conn.close()

def get_id(symbol, interval, start_date) -> int:
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.execute("SELECT id FROM bots WHERE symbol=%s AND interval=%s AND start_date=%s;",
                    (symbol, interval, start_date))
        return cur.fetchone()[0]
    
    except:
        print("Error while getting id")
    
    finally:
        if conn:
            conn.close()

def exists_klines(bot_id: int) -> bool:
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.execute("SELECT bot_id FROM klines WHERE bot_id = %s;", (bot_id, ))
        if cur.fetchone() is None:
            return False
        
        return True
    
    except:
        print("Error while checking for registered klines")
    
    finally:
        if conn:
            conn.close()
    

def get_klines_info(bot_id: int):
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.execute("SELECT symbol, interval, start_date FROM bots WHERE id = %s;", (bot_id,))
        return cur.fetchone()
    
    except:
        print("Error while getting klines info")
    
    finally:
        if conn:
            conn.close()
    
def push_klines(klines: list):
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.executemany("""INSERT INTO klines (bot_id, open_time, open_value, high, low,
                        close_value, volume, close_time, quote_asset_volume, trades_number,
                        taker_buy_base,taker_buy_quote) 
                        VALUES  (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""", klines)
        conn.commit()
    
    except:
        print("Error while pushing klines")
    
    finally:
        if conn:
            conn.close()

def get_last_date(bot_id: int) -> int:
    try:
        conn = psycopg2.connect("dbname=tradingbot user=postgres password=root")
        cur = conn.cursor()
        cur.execute("""SELECT close_time FROM klines WHERE bot_id = %s
                    ORDER BY close_time DESC LIMIT 1;""", (bot_id,))
        return cur.fetchone()[0]
    
    except:
        print("Error while getting last date")
    
    finally:
        if conn:
            conn.close()
