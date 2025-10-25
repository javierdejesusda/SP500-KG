from rdflib import Namespace

ONT = Namespace("http://example.org/sp500-ontology#")
DATA = Namespace("http://example.org/sp500-data/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

ONTOLOGY_FILE = "sp500_ontology.ttl"
OUTPUT_FILE = "sp500_full_graph.ttl"

WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
USER_AGENT_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

TEST_MODE_LIMIT = 10 

FRED_SYMBOLS = {
    'FEDFUNDS': 'Tasa_Interes_Federal',
    'CPIAUCSL': 'Inflacion_CPI'
}

SENSITIVITY_MAP = {
    'Technology': 'FEDFUNDS',
    'Information Technology': 'FEDFUNDS', 
    'Financial Services': 'FEDFUNDS',
    'Financials': 'FEDFUNDS',
    'Real Estate': 'FEDFUNDS',
    'Healthcare': 'CPIAUCSL',
    'Energy': 'CPIAUCSL',
    'Consumer Defensive': 'CPIAUCSL',
    'Consumer Staples': 'CPIAUCSL'
}