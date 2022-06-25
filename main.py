from functions import *
from models import *
import colorama
from openpyxl import Workbook
from tkinter import *

global filename

def main(list):

    wb = Workbook() # initialize excel workbook
    initWorkbook(wb)

    colorama.init() # init colorama

    config = getConfig()

    fund_data = []
    wb_pin = 5

    url = "https://www.morningstar.it/it/funds/snapshot/snapshot.aspx?id="
    
    codeList = list

    for code in codeList:
        fund_data = []

        for tab in config:
            source = getHtmlSource(url, code, tab.query_bit)
            source = parseHtmlSource(source)
            fund_data.append(extractData(tab, source))

        fund_data = prepareDataForExcel(fund_data)
        writeToExcel(fund_data, wb, wb_pin)
        wb_pin += 1
        
        # print(colored("{id} DONE!", 'yellow').format(id = code.strip()))

    

# if __name__ == '__main__':
#     root = Tk()
#     root.title("Fund Info Gathering App")
#     root.geometry("700x300")
#     root.resizable(width=False, height=False)
#     root.columnconfigure(1, weight=1)
#     root.columnconfigure(2, weight=1)
#     root.columnconfigure(3, weight=1)
#     root.rowconfigure(1, weight=1)
#     root.rowconfigure(2, weight=1)
#     root.rowconfigure(3, weight=1)

#     filename = filedialog.askopenfile(parent=root, mode='r', title='Choose a file').name

#     lbl1 = Label(root, text=filename, font=("Arial", 15))
#     lbl1.grid(column=2, row=0)
   

#     if filename != None:
#         btn2 = Button(root, text = 'Comincia analisi', command = lambda:main(filename), width=30, height=10)
#         btn2.grid(column=2, row=2)


#     root.mainloop()
