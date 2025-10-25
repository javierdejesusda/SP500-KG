import config
import sys

def add_expert_relations(graph, sector_uris, indicator_uris):
    added_relations = 0
    
    for sector_name, indicator_symbol in config.SENSITIVITY_MAP.items():
        if sector_name in sector_uris and indicator_symbol in indicator_uris:
            sector_uri = sector_uris[sector_name]
            indicator_uri = indicator_uris[indicator_symbol]
            
            graph.add((sector_uri, config.ONT.esSensibleA, indicator_uri))
            added_relations += 1