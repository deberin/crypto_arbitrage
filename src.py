from neo4j import GraphDatabase
from neo4j.exceptions import DriverError, Neo4jError

class Arbitrage:
    def __init__(self, uri, user, password, database=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
        
    def close(self):
        self.driver.close()
        
    def clear(self):
        self.run("MATCH (n) DETACH DELETE n")
    
   
    def import_market(self, data):
        set_coin = set()
        for key, item in data.items():
            set_coin.update((item['coin1'], item['coin2']))
            
        self.run(f"UNWIND {list(set_coin)} as c "
                 "MERGE (a:coin {name:c})")
        
        self.run(f"CREATE INDEX coin_name IF NOT EXISTS FOR (p:coin) ON (p.name)")
        
        #Delete existing relations 
        self.run(f"MATCH (n)-[r:EXCHANGE]->() DELETE r")
        
        #Create new relation
        with self.driver.session(database=self.database) as session:
            tx = session.begin_transaction()
            for key, item in data.items():
                  tx.run(f"MATCH (a:coin {{name:'{item['coin1']}'}}) "
                         f"MATCH (b:coin {{name:'{item['coin2']}'}}) "
                         f"CREATE (a)-[:EXCHANGE {{price:{item['bidPrice']}}}]->(b) "
                         f"CREATE (b)-[:EXCHANGE {{price:{item['askPrice']}}}]->(a) ")
                
            try:   
                tx.commit()
            except:  
                raise
            
    def get_arbitrage_bundles(self, max_length=3, limit=3, coin='USDT'):
        records, summary, keys = self.run("WITH 100 AS startVal "
                          f"MATCH x = (c:coin)-[r:EXCHANGE*..{max_length}]->(c) "
                          f"WHERE c.name = '{coin}' "
                          "WITH x, r, REDUCE(s = startVal, e IN r | s * e.price) AS endVal, startVal "
                          "WHERE endVal > startVal "
                          "RETURN [n IN NODES(x) | n.name] AS Exchanges, endVal - startVal AS Profit "
                          "ORDER BY Profit DESC "
                          f"LIMIT {limit} ")
        
        res = []
        for r in records:
            res.append([r['Exchanges'], r['Profit']])
            
        return res
        
    
    def run(self, query):
        try:
            record = self.driver.execute_query(query, database_=self.database)
            return record
        # Capture any errors along with the query and data for traceability
        except (DriverError, Neo4jError) as exception:
            raise
    

def validate_markets(markets:dict)->dict:
    
    #remove pair without rates
    for key, value in markets.items():
        if 'bidPrice' not in value or 'askPrice' not in value:
            del markets[key]
            
    return markets          