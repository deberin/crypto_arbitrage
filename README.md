
# Searching for arbitrage bundles on a crypto exchange in Python

An example of how you can search for mappings in Python and graph-based databases. This approach is used here [0xdeberin.com](http://0xdeberin.com)


## Usage/Examples
To work, you will need to install [NEO4j graph database](https://neo4j.com/) and Neo4j driver for Python.


```Python
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
    
    
```


## Roadmap

- Connect other exchanges for example

