from functions import *
from models import *
import colorama
from openpyxl import Workbook

def getConfig():

    searched1 = [MsTable("overviewQuickstatsDiv", ["Categoria Assogestioni", "Var.Ultima Quotazione", "Isin"]), MsTable("overviewPortfolioTopRegionsDiv", [2]), MsTable("overviewPortfolioTopSectorsDiv", [3])]
    tab1 = MsTab("general", "", searched1)

    searched2 = [MsTable("returnsTrailingDiv", ["YTD", "1-Anno", "3-Anni Ann.ti", "5-Anni Ann.ti"])]
    tab2 = MsTab("rendimenti", "&tab=1", searched2)

    searched3 = [MsTable("ratingRiskDiv", ["Deviazione Std.", "Rendimento Medio", "", "5-Anni Ann.ti"]), MsTable("ratingRiskRightDiv", ["Indice di Sharpe"]), MsTable("ratingMptStatsDiv", ["Beta", "Alfa"])]
    tab3 = MsTab("rating e Rischio", "&tab=2", searched3)

    searched5 = [MsTable("managementFeesDiv", ["Entrata (max)", "Uscita (max)", "Switch (max)"]), MsTable("managementFeesAnnualChargesDiv", ["Gestione (max)", "Spese correnti"]), MsTable("managementPurchaseInformationDiv", ["Ingresso"])]
    tab5 = MsTab("commissioni", "&tab=5", searched5)

    return [tab1, tab2, tab3, tab5]


def main():

    wb = Workbook() # initialize excel workbook
    initWorkbook(wb)

    colorama.init() # init colorama

    config = getConfig()

    fund_data = []
    wb_pin = 5

    url = "https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id="
    
    codeList = []
    with open("list.txt", "r") as file:
        for line in file:
            codeList.append(line)

    for code in codeList:
        fund_data = []

        for tab in config:
            source = getHtmlSource(url, code, tab.query_bit)
            source = parseHtmlSource(source)
            fund_data.append(extractData(tab, source))

        fund_data = prepareDataForExcel(fund_data)
        writeToExcel(fund_data, wb, wb_pin)
        wb_pin += 1



if __name__ == '__main__':
    main()