import requests
from bs4 import BeautifulSoup
from termcolor import colored
from models import *

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

def getHtmlSource(url, code, query_bit):

    #print(colored("[SYSTEM] ", 'green') + "Fetching: {code} - {t} ".format(code = code.strip(), t = query_bit))

    if query_bit:
        response = requests.get(url=url+code+query_bit)
    else:
        response = requests.get(url=url+code)

    #print(colored("[SYSTEM]", 'green') + colored("-(STATUS)", 'blue') + " {code} OK".format(code = response.status_code))

    return response.text
    


def parseHtmlSource(source):

    #print(colored("[SYSTEM]", 'green') +" Parsing page source code")

    soup = BeautifulSoup(source, 'html.parser')

    return soup



def saveObject(obj):
    jsonstr = obj.toJSON()
    with open("config.json", "a") as f:
        f.write(jsonstr)



def extractData(tab, source):
    '''Extracts the required data from the html source'''
    fund_data = [] # the final dataset

    # get fund name
    if not tab.query_bit:
        x = source.find(class_='snapshotTitleBox')
        x = x.find('h1')
        fund_data.append(x.text)

    for s in tab.searched:
        id = s.div_id #set the div id to search
        tb = source.find('div', {"id": id}) #find all dv with id == div_id
        
        if not tb:
            print(colored("[ERROR]", 'red') + " Invalid div_id paramether")
            return fund_data

        # for every row specified in s.rows, finds the one in the table with the matching
        # header and adds it to the list
        if s.rows:
            if len(s.rows) == 1 and isinstance(s.rows[0], int):
                #get first n rows of table

                found = tb.find_all('tr') #extract all lines of the table
                raw_output = [] # to store the rows still in html
                extracted_rows = []

                n = s.rows[0]
                i = 0
                for tr in found: # for each row in the ones found earlier
                    if i == n+1:
                        break
                    if i != 0:
                        raw_output.append(tr)
                    i+=1
                
                for raw in raw_output:
                    row = []
                    for segment in raw: # extract and clean text inside
                            data = (segment.text).replace(u'\xa0', '').replace('\n', '').strip()
                            if data: 
                                row.append(data) # reconstruct the row
                    extracted_rows.append(row) # append the final row in the list

                fund_data.append(extracted_rows) # append extracted rows to final data

            else:
                #get specified rows of table
                extracted_rows = []
                for head_title in s.rows:

                    found = tb.find_all('tr') #extract all lines of the table
                    raw_output = [] # to store the rows still in html
                    for tr in found: # for each row in the ones found earlier
                        for td in tr: # for each cell of the row
                            if td.text == head_title: # if the text is == head_title append it to the list
                                raw_output.append(tr)
                                break
                        
                    for raw in raw_output: #for every raw row appended earlier
                        row = []
                        for segment in raw: # extract and clean text inside
                            data = (segment.text).replace(u'\xa0', '').replace('\n', '').replace('%', '').strip()
                            if data: 
                                row.append(data) # reconstruct the row
                        extracted_rows.append(row) # append the final row in the list
                
                fund_data.append(extracted_rows) # append extracted rows to final data
        else:
            #get all table
            pass
        
    return fund_data



def prepareDataForExcel(fund_data):
    final_data = {}

    final_data['nome'] = fund_data[0][0]
    del fund_data[0][0]

    for tab in fund_data:
        
        for table in tab:
            for row in table:
                header = row[0]
                values = []
                for value in row[1:]:
                    values.append(value)
                final_data[header] = values

    
    return final_data


def writeToExcel(data, wb, wb_pin):
    sheet = wb.active
    i = wb_pin

    dict_list = list(data.keys())
        
    sheet.cell(row=i, column=1).value = data["Isin"][0]
    sheet.cell(row=i, column=2).value = data["nome"]
    sheet.cell(row=i, column=4).value = data["Alfa"][0]
    sheet.cell(row=i, column=5).value = data["Indice di Sharpe"][0]
    sheet.cell(row=i, column=6).value = data["Deviazione Std."][0]
    sheet.cell(row=i, column=7).value = data["Rendimento Medio"][0]
    sheet.cell(row=i, column=8).value = data["Beta"][0]

    sheet.cell(row=i, column=10).value = data["YTD"][0]
    sheet.cell(row=i, column=11).value = data["1-Anno"][0]
    sheet.cell(row=i, column=12).value = data["3-Anni Ann.ti"][0]
    
    try:
        sheet.cell(row=i, column=13).value = data["5-Anni Ann.ti"][0]
    except:
        sheet.cell(row=i, column=13).value = "n/a"

    sheet.cell(row=i, column=14).value = "n/a"


    sheet.cell(row=i, column=16).value = data["Entrata (max)"][0]
    sheet.cell(row=i, column=17).value = data["Uscita (max)"][0]
    sheet.cell(row=i, column=18).value = data["Switch (max)"][0]
    sheet.cell(row=i, column=19).value = data["Gestione (max)"][0]
    sheet.cell(row=i, column=20).value = data["Spese correnti"][0]

    sheet.cell(row=i, column=22).value = dict_list[4] + " | " + data[dict_list[4]][0] + "%"
    sheet.cell(row=i, column=23).value = dict_list[5] + " | " + data[dict_list[5]][0] + "%"
    sheet.cell(row=i, column=26).value = dict_list[6] + " | " + data[dict_list[6]][0] + "%"
    sheet.cell(row=i, column=27).value = dict_list[7] + " | " + data[dict_list[7]][0] + "%"
    sheet.cell(row=i, column=28).value = dict_list[8] + " | " + data[dict_list[8]][0] + "%"
        
    wb.save("Funds_analysis.xlsx")



def initWorkbook(wb):
    sheet = wb.active

    sheet.cell(row=4, column=4).value = "Alfa"
    sheet.cell(row=4, column=5).value = "Sharp ratio"
    sheet.cell(row=4, column=6).value = "Volatilità"
    sheet.cell(row=4, column=7).value = "Rendimento medio"
    sheet.cell(row=4, column=8).value = "Beta"

    sheet.cell(row=4, column=10).value = "YTD"
    sheet.cell(row=4, column=11).value = "1 Year"
    sheet.cell(row=4, column=12).value = "3 Years"
    sheet.cell(row=4, column=13).value = "5 Years"
    sheet.cell(row=4, column=14).value = "BM"

    sheet.cell(row=4, column=16).value = "In"
    sheet.cell(row=4, column=17).value = "Out"
    sheet.cell(row=4, column=18).value = "Switch"
    sheet.cell(row=4, column=19).value = "Gestione"
    sheet.cell(row=4, column=20).value = "Ongoing charge"
    sheet.cell(row=4, column=22).value = "Top 2 region"
    sheet.cell(row=4, column=26).value = "Top 3 sectors"

    wb.save("Funds_analysis.xlsx")