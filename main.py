import sys
import config
from utils import get_http_session
from graph_manager import GraphManager
from extractors.wikipedia import WikipediaExtractor
from extractors.yfinance import YFinanceEnricher
from extractors.fred import FredCollector
from populators.relations import add_expert_relations

def main(test_mode=True):
    limit = config.TEST_MODE_LIMIT if test_mode else None
    
    session = get_http_session()
    graph_mgr = GraphManager(config.ONTOLOGY_FILE)
    g = graph_mgr.get_graph()

    try:
        wiki_extractor = WikipediaExtractor(session)
        df_companies = wiki_extractor.get_sp500_list(limit=limit)
        company_uris, sector_uris = wiki_extractor.populate_graph(g, df_companies)

        yfinance_enricher = YFinanceEnricher()
        yfinance_enricher.enrich_companies(g, company_uris)

        fred_collector = FredCollector(session)
        indicator_uris = fred_collector.get_macro_data(g)

        add_expert_relations(g, sector_uris, indicator_uris)

        graph_mgr.serialize(config.OUTPUT_FILE)

    finally:
        session.close()

if __name__ == "__main__":
    run_in_test_mode = '--full' not in sys.argv
    main(test_mode=run_in_test_mode)