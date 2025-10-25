import pandas_datareader.data as pdr
from datetime import datetime, timedelta
import config
import sys
from rdflib import Literal

class FredCollector:
    def __init__(self, http_session):
        self.session = http_session

    def get_macro_data(self, graph):
        indicator_uris = {}
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        for symbol, label in config.FRED_SYMBOLS.items():
            try:
                data = pdr.get_data_fred(symbol, start_date, end_date, session=self.session)
                if data.empty:
                    continue
                    
                latest_values = data[symbol].dropna()
                if latest_values.empty:
                    continue

                latest_value = latest_values.iloc[-1]
                latest_date = latest_values.index[-1].date()
                
                indicator_uri = config.DATA[symbol]
                indicator_uris[symbol] = indicator_uri
                
                graph.add((indicator_uri, config.RDF.type, config.ONT.IndicadorMacroeconómico))
                graph.add((indicator_uri, config.RDFS.label, Literal(label)))
                graph.add((indicator_uri, config.ONT.valor, Literal(latest_value, datatype=config.XSD.decimal)))
                graph.add((indicator_uri, config.ONT.fecha, Literal(latest_date, datatype=config.XSD.date)))
                
            except Exception:
                continue # Silently skip failed symbols
                
        return indicator_uris