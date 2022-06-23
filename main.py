from functions import *
from models import *
import json

def main():
    url = "https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id="
    code = "F0GBR04AG0"
    source = getHtmlSource(url, code)

    source = parseHtmlSource(source)

    searched = [MsTable("overviewQuickstatsDiv", ["Categoria Assogestioni", "Var.Ultima Quotazione", "Isin", "Entrata (max)"]), MsTable("overviewPortfolioTopRegionsDiv", ["Europa Occidentale - Euro"]), MsTable("overviewPortfolioTopSectorsDiv", [3]), MsTable("TrailingReturnsOverview", ["YTD", "3-Anni Ann.ti"])]
    tab1 = MsTab("general", "", searched)

    extractData(tab1, source)

if __name__ == '__main__':
    main()