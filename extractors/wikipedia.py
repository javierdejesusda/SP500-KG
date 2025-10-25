import pandas as pd
import config
import sys
import requests
from io import StringIO
from rdflib import Literal

class WikipediaExtractor:
    def __init__(self, http_session):
        self.session = http_session

    def get_sp500_list(self, limit=None):
        try:
            response = self.session.get(config.WIKIPEDIA_URL)
            response.raise_for_status()
            
            tables = pd.read_html(StringIO(response.text))
            df_sp500 = tables[0]
            
            if limit:
                df_sp500 = df_sp500.head(limit)
                
            return df_sp500
            
        except requests.exceptions.RequestException:
            print("Error HTTP extrayendo la tabla de Wikipedia.", file=sys.stderr)
            sys.exit(1)
        except Exception:
            print("Error procesando la tabla de Wikipedia.", file=sys.stderr)
            sys.exit(1)

    def populate_graph(self, graph, df_sp500):
        company_uris = {}
        sector_uris = {}
        
        sp500_index_uri = config.DATA["SP500"]
        graph.add((sp500_index_uri, config.RDF.type, config.ONT.ÍndiceBursátil))
        graph.add((sp500_index_uri, config.RDFS.label, Literal("S&P 500 Index", lang="en")))

        for _, row in df_sp500.iterrows():
            ticker = str(row['Symbol']).replace('.', '-')
            label = str(row['Security'])
            sector_name = str(row['GICS Sector'])
            
            company_uri = config.DATA[ticker]
            sector_uri = config.DATA[sector_name.replace(' ', '_').replace('&', 'and')]
            
            if ticker not in company_uris:
                company_uris[ticker] = company_uri
                
                graph.add((company_uri, config.RDF.type, config.ONT.Compañía))
                graph.add((company_uri, config.ONT.tickerSymbol, Literal(ticker)))
                graph.add((company_uri, config.ONT.nombreOficial, Literal(label, lang="en")))
                graph.add((company_uri, config.ONT.esConstituyenteDe, sp500_index_uri))
                
                if sector_name not in sector_uris:
                    sector_uris[sector_name] = sector_uri
                    graph.add((sector_uri, config.RDF.type, config.ONT.SectorEconómico))
                    graph.add((sector_uri, config.RDFS.label, Literal(sector_name)))
                
                graph.add((company_uri, config.ONT.perteneceAlSector, sector_uri))
        
        return company_uris, sector_uris