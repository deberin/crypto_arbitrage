from exchange import Binance
from src import Arbitrage


def main():
    tikers = Binance().ticker()
    
    #Need create Neo4j database or use default
    arb = Arbitrage("bolt://localhost", user='<db_user>', password='<db_password>', database='neo4j')
    arb.import_market(tikers)
    res= arb.get_arbitrage_bundles(max_length=3, limit=5, coin='USDT')
    
    for i in res:
        print(f'Path:{i[0]}, profit:{round(i[1],2)}%')



if __name__ == '__main__':
    main()
    
    