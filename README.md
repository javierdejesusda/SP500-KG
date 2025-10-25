# S&P 500 Knowledge Graph (SP500-KG)

This project automatically extracts, transforms, and loads (ETL) data from S&P 500 companies, their financial reports, and relevant macroeconomic indicators to build a Knowledge Graph in RDF format.

The resulting graph (`sp500_full_graph.ttl`) uses the ontology defined in `sp500_ontology.ttl` and is ready to be queried with SPARQL using a server like Apache Fuseki.

## Features

* **Company Extraction**: Fetches the updated list of S&P 500 companies and their sectors from Wikipedia.
* **Data Enrichment**: For each company, it fetches detailed data from Yahoo Finance (`yfinance`), including:
    * Descriptive data (summary, country, employees, website).
    * Key metrics (Market Cap, P/E Ratio).
    * Current CEO.
    * Data from the latest annual financial report (Revenue, Net Income, Assets, etc.).
* **Macroeconomic Data**: Fetches the latest values for key indicators (Federal Funds Rate and CPI) from FRED.
* **Custom Ontology**: Data is structured according to an OWL ontology (`sp500_ontology.ttl`) that defines the classes and relationships (e.g., `Compañía`, `ReporteFinanciero`, `perteneceAlSector`, `esSensibleA`).

## Project Structure

* `main.py`: Main entry point for the ETL pipeline.
* `config.py`: Central configuration file (URLs, namespaces, API keys, etc.).
* `graph_manager.py`: Class to manage RDF graph creation, loading, and serialization.
* `utils.py`: Helper functions (e.g., robust HTTP session, `add_literal_safe`).
* `extractors/`: Modules responsible for extracting data from various sources (Wikipedia, yfinance, FRED).
* `populators/`: Modules for adding expert knowledge (e.g., `relations.py` which links sectors to indicators).
* `sp500_ontology.ttl`: The OWL ontology that defines the graph's structure.
* `requirements.txt`: Python dependencies.

## Installation

Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The `main.py` script has two execution modes:

1.  **Test Mode**:
    Processes only the first 10 companies. This is fast and useful for verifying that everything works.
    ```bash
    python main.py
    ```

2.  **Full Mode**:
    Processes all S&P 500 companies. This may take several minutes.
    ```bash
    python main.py --full
    ```

In both cases, the script will generate (or overwrite) the `sp500_full_graph.ttl` file in the root folder.

## How to Query the Data (with Apache Fuseki)

1.  **Start a Fuseki server:** Download [Apache Jena Fuseki](https://jena.apache.org/download/index.html) and run it.
2.  **Create a Dataset:** Go to `http://localhost:3030`, click "manage datasets" > "add new dataset" (e.g., name it `sp500`).
3.  **Upload the Graph:** In your `sp500` dataset panel, go to "Upload Data" and upload the `sp500_full_graph.ttl` file (leave it in the "default" graph).
4.  **Query with SPARQL:** Go to the "Query" tab and run your queries.

### SPARQL Query Example

**Which companies have a Market Cap greater than 400 billion?**

```sparql
PREFIX sp500-ont: [http://example.org/sp500-ontology#](http://example.org/sp500-ontology#)

SELECT ?ticker ?nombre ?marketCap
WHERE {
  ?compania a sp500-ont:Compañía .
  ?compania sp500-ont:tickerSymbol ?ticker .
  ?compania sp500-ont:nombreOficial ?nombre .
  ?compania sp500-ont:capitalizacionMercado ?marketCap .
  
  # Filter the results numerically
  FILTER(?marketCap > 400000000000)
}
