import requests
from bs4 import BeautifulSoup
from sqlalchemy import column
from termcolor import colored

def getHtmlSource(url, code, query_bit):

    print(colored("[SYSTEM] ", 'green') + "Fetching: {code} - {tab}".format(code = code, tab = query_bit))

    if query_bit:
        response = requests.get(url=url+code+query_bit)
    else:
        response = requests.get(url=url+code)

    print(colored("[SYSTEM]", 'green') + colored("-(STATUS)", 'blue') + " {code}".format(code = response.status_code))

    return response.text
    


def parseHtmlSource(source):

    print(colored("[SYSTEM]", 'green') +" Parsing page source code")

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
    # if not tab.query_bit:
    #     x = source.find(class_='snapshotTitleBox')
    #     x = x.find('h1')
    #     fund_data.append(x.text)

    for s in tab.searched:
        id = s.div_id #set the div id to search
        tb = source.find('div', {"id": id}) #find all dv with id == div_id
        
        if not tb:
            print(colored("[ERROR]", 'red') + " Invalid div_id paramether")
            exit(1)

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

    for tab in fund_data:
        for table in tab:
            for row in table:
                header = row[0]
                values = []
                for value in row[1:]:
                    values.append(value)
                final_data[header] = values

    return final_data


def writeToExcel(data, wb):
    sheet = wb.active

    col_refs = [4,5,6,7,8,10,11,12,13,14,16,17,18,19,20]

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

    i = 0
    i_row = 0
    i_col = 0
    for row in data:
        if i == 0:
            sheet.cell(row=6, column=2).value = data[0]
            pass
        
        print(row)
        i += 1
        



    wb.save("Funds_analysis.xlsx")