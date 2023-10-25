import requests
from src import validate_markets

class Binance:
    BASE_ENDPOINT = "https://api.binance.com"
    
    def __init__(self):
        pass
    
    def request(self, endpoint):
        try:
            req = requests.get(self.BASE_ENDPOINT+endpoint)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)
        
        if req.status_code != 200:
            req.raise_for_status()
        
        return req.json()        
        
    def ticker(self):
      trade_pairs = self.request("/api/v3/exchangeInfo?permissions=SPOT" )
      
      markets = {}
      #Bring to one UPPERCASE format
      """ {symbol : {'s' : 'coin1_coin2',
                     'coin1'  : 'coin1',
                     'coin2'  : 'coin2'}}"""
      for symbol in trade_pairs['symbols']:
         if symbol['status'] != 'TRADING':
             continue
         markets[symbol['symbol']] = ({'s':f"{symbol['baseAsset']}_{symbol['quoteAsset']}",
                                       'coin1':symbol['baseAsset'],
                                       'coin2':symbol['quoteAsset']})
         
         
      #Adding an exchange rate
      rate = self.request("/api/v3/ticker/price")
      """
      ....
      'bidPrice': float
      'askPrice': float
      """
      
      for r in rate:
          try:
            markets[r['symbol']].update({'bidPrice':float(r['price']), 
                                         'askPrice': 1/float(r['price'])}) 
          except:
              continue  
          
      
      #remove pair without rates    
      return validate_markets(markets)
         
         