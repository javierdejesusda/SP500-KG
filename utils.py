import sys
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from rdflib import Literal, URIRef
import config

def get_http_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods={"HEAD", "GET", "OPTIONS"}
    )
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update(config.USER_AGENT_HEADER)
    return session

def add_literal_safe(graph, subject, predicate, data, data_key, datatype=config.XSD.string, round_digits=None):
    if data_key in data and pd.notna(data[data_key]):
        value = data[data_key]
        
        if round_digits is not None:
            try:
                value = round(float(value), round_digits)
            except (ValueError, TypeError):
                return
        
        if datatype == config.XSD.anyURI:
             if isinstance(value, str) and value.startswith("http"):
                 graph.add((subject, predicate, URIRef(value)))
        else:
             graph.add((subject, predicate, Literal(value, datatype=datatype)))