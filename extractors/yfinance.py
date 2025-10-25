import yfinance as yf
import pandas as pd
from utils import add_literal_safe
import config
import sys
from rdflib import Literal

class YFinanceEnricher:
    def __init__(self):
        self.ceo_uris = {}

    def enrich_companies(self, graph, company_uris):
        for i, (ticker, company_uri) in enumerate(company_uris.items()):
            
            # Silently skip tickers that fail
            try:
                company_obj = yf.Ticker(ticker)
                
                if not company_obj.info:
                    continue
                    
                self._add_company_info(graph, company_uri, company_obj.info)
                self._add_financial_reports(graph, company_uri, company_obj, ticker)
                
            except Exception:
                continue 
                
        return self.ceo_uris

    def _add_company_info(self, graph, company_uri, info):
        officers = info.get('companyOfficers', [])
        if officers:
            ceo_name = officers[0].get('name')
            if ceo_name:
                ceo_key = ceo_name.replace(' ', '_').replace('.', '').replace(',', '')
                ceo_uri = config.DATA[ceo_key]
                
                if ceo_name not in self.ceo_uris:
                    self.ceo_uris[ceo_name] = ceo_uri
                    graph.add((ceo_uri, config.RDF.type, config.ONT.Ejecutivo))
                    graph.add((ceo_uri, config.ONT.nombreOficial, Literal(ceo_name)))
                graph.add((company_uri, config.ONT.tieneCEO, ceo_uri))

        add_literal_safe(graph, company_uri, config.ONT.resumenEmpresarial, info, 'longBusinessSummary')
        add_literal_safe(graph, company_uri, config.ONT.sitioWeb, info, 'website', config.XSD.anyURI)
        add_literal_safe(graph, company_uri, config.ONT.numeroEmpleados, info, 'fullTimeEmployees', config.XSD.integer)
        add_literal_safe(graph, company_uri, config.ONT.capitalizacionMercado, info, 'marketCap', config.XSD.long)
        add_literal_safe(graph, company_uri, config.ONT.ratioPER, info, 'trailingPE', config.XSD.decimal, 4)
        add_literal_safe(graph, company_uri, config.ONT.pais, info, 'country')
        add_literal_safe(graph, company_uri, config.ONT.ciudad, info, 'city')

        if 'dividendYield' in info and pd.notna(info['dividendYield']):
            div_yield = info['dividendYield'] * 100
            graph.add((company_uri, config.ONT.rentabilidadDividendo, 
                       Literal(round(div_yield, 4), datatype=config.XSD.decimal)))

    def _add_financial_reports(self, graph, company_uri, company_obj, ticker):
        financials = company_obj.financials
        if financials.empty:
            return
            
        latest_report = financials.iloc[:, 0]
        report_date = latest_report.name.date()
        report_date_str = report_date.strftime('%Y-%m-%d')
        
        report_uri = config.DATA[f"Report_{ticker}_{report_date_str}"]
        
        graph.add((report_uri, config.RDF.type, config.ONT.ReporteFinanciero))
        graph.add((company_uri, config.ONT.tieneReporte, report_uri))
        graph.add((report_uri, config.ONT.reporteDe, company_uri))
        graph.add((report_uri, config.ONT.fechaReporte, Literal(report_date, datatype=config.XSD.date)))
        graph.add((report_uri, config.ONT.esDeTipo, Literal("Annual", lang="en")))
        
        add_literal_safe(graph, report_uri, config.ONT.ingresosTotales, latest_report, 'Total Revenue', config.XSD.long)
        add_literal_safe(graph, report_uri, config.ONT.beneficioBruto, latest_report, 'Gross Profit', config.XSD.long)
        add_literal_safe(graph, report_uri, config.ONT.ebit, latest_report, 'EBIT', config.XSD.long)
        add_literal_safe(graph, report_uri, config.ONT.beneficioNeto, latest_report, 'Net Income', config.XSD.long)

        balance_sheet = company_obj.balance_sheet
        if not balance_sheet.empty:
            latest_bs = balance_sheet.iloc[:, 0]
            add_literal_safe(graph, report_uri, config.ONT.activosTotales, latest_bs, 'Total Assets', config.XSD.long)
            add_literal_safe(graph, report_uri, config.ONT.pasivosTotales, latest_bs, 'Total Liab', config.XSD.long)
        
        cashflow = company_obj.cashflow
        if not cashflow.empty:
            latest_cf = cashflow.iloc[:, 0]
            add_literal_safe(graph, report_uri, config.ONT.flujoDeCajaOperativo, latest_cf, 'Total Cash From Operating Activities', config.XSD.long)