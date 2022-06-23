from attr import attrs
from numpy import character
import requests
from bs4 import BeautifulSoup

def getHtmlSource(url, code):

    print("[SYSTEM] Fetching: {code}".format(code = code))

    response = requests.get(url=url+code)

    print("[SYSTEM]-(STATUS) {code}".format(code = response.status_code))

    return response.text
    


def parseHtmlSource(source):

    print("[SYSTEM] Parsing page source code")

    soup = BeautifulSoup(source, 'html.parser')

    return soup



def saveObject(obj):
    jsonstr = obj.toJSON()
    with open("config.json", "w+") as f:
        f.write(jsonstr)



def extractData(tab, source):
    
    for s in tab.searched:
        id = s.div_id
        tb = source.find('div', {"id": id})
        
        if s.rows:
            if len(s.rows) == 1 and isinstance(s.rows[0], int):
                #get first n rows of table
                pass
            else:
                #get specified rows of table
                extracted_rows = []
                for head_title in s.rows:
                    
                    found = tb.find_all('tr')
                    raw_output = []
                    for tr in found:
                        for td in tr:
                            if td.text == head_title:
                                raw_output.append(tr)
                        
                    for raw in raw_output:
                        row = []
                        for segment in raw:
                            data = (segment.text).replace(u'\xa0', '').replace('\n', '').strip()
                            if data:
                                row.append(data)
                        extracted_rows.append(row)
                
                print(extracted_rows)
        else:
            #get all table
            pass
        
