# Trading bot
It's a python bot that gets candlestick data from binance API (official page https://binance-docs.github.io/apidocs/spot/en/#change-log) and is able to perform a variety of algorithmic trading strategies. This bot also uses sentimental analysis and machine learning algorithms in order to make better trade decisions.  
This project uses the following github repo to get the data from the API: https://github.com/sammchardy/python-binance we are not related in any way, I use the module developed by him for simplicity. 

## Important
This project is still under developement and is still not ready to perform everything in the previous description, use it under your own responability.  

## About the candlestick data
Data is downloaded from binance API version 3, to get access to it you have to register on the official site (https://www.binance.com/en) and then generate the API public and private keys.  
To use the bot without errors or inconvenients, create a python file named "keys.py" and write your keys in the next format:  
api_key = "your public key"  
api_secret = "your private key"  
The bot will look for those exact names, otherwise you will have to make some modifications to the code.  

## About the Database
The project uses postgreSQL to store all the data, you can see documentation about psql here https://www.postgresql.org/, I strongly recommend taking a moment to read the docs before start working with this project.  
The DB settings are set as follows:  
- User: postgres  
- DB name: tradingbot  
- Tables: klines, bots, orders
- Password: root

To change it, modify the CRUD.py file, no more actions are required.
