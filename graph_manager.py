from rdflib import Graph
import config
import sys

class GraphManager:
    def __init__(self, ontology_path):
        self.g = Graph()
        self.bind_namespaces()
        self.load_ontology(ontology_path)

    def bind_namespaces(self):
        self.g.bind("sp500-ont", config.ONT)
        self.g.bind("sp500-data", config.DATA)
        self.g.bind("owl", config.OWL)
        self.g.bind("rdfs", config.RDFS)
        self.g.bind("rdf", config.RDF)
        self.g.bind("xsd", config.XSD)

    def load_ontology(self, path):
        try:
            self.g.parse(path, format="turtle")
        except FileNotFoundError:
            print(f"Error: El archivo de ontología '{path}' no se encontró.", file=sys.stderr)
            sys.exit(1)
        except Exception:
            print(f"Error al parsear la ontología '{path}'.", file=sys.stderr)
            sys.exit(1)

    def get_graph(self):
        return self.g

    def serialize(self, destination_file):
        try:
            self.g.serialize(destination=destination_file, format="turtle")
            print(f"Grafo guardado en '{destination_file}'.")
        except Exception:
            print(f"Error al serializar el grafo.", file=sys.stderr)
            sys.exit(1)