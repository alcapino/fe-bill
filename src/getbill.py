from PyPDF2 import PdfReader
from settings import DOCS_ROOT, GCREDS
import pygsheets, re
import pandas as pd

month = "FEB"
reader = PdfReader(DOCS_ROOT + month + ".pdf")
number_of_pages = len(reader.pages)
text = ""
for i in range(number_of_pages):
    page = reader.pages[i]
    text += page.extract_text()

# # print(text)
# f = open("temp.txt", "w")
# f.write(text)
# f.close()
# print("temp file written!")

# query since 14 Feb 10PM
# Factuurnummer:\s*(?P<invoice_num>\d*)[\s\S]+Vervaldatum:\s*(?P<due_date>[\d\-]+)[\s\S]+Termijnfactuur\s*(?P<month>\w*)[\s\S]+Vaste leveringskosten\s+(?P<present_period>[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2})[\s\S]{3}(?P<del_cost_novat>(?<=\n\€\n)[\d\,]+)[\s\S]{3}(?P<del_cost_wvat>(?<=\n\€\n)[\d\,]+)[\s\S]+ODE[\s\S]{1}[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2}[\s\S]{3}(?P<ode_novat>(?<=\n\€\n)[\d\,]+)[\s\S]{3}(?P<ode_wvat>(?<=\n\€\n)[\d\,]+)
query = re.compile(
    'Factuurnummer:\s*'
    '(?P<invoice_num>\d*)[\s\S]+Vervaldatum:\s*'
    '(?P<due_date>[\d\-]+)[\s\S]+Termijnfactuur\s*'
    '(?P<month>\w*)[\s\S]+Vaste leveringskosten\s+'
    '(?P<present_period>[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2})[\s\S]{3}'
    '(?P<del_cost_novat>(?<=\n\€\n)[\d\,]+)[\s\S]{3}'
    '(?P<del_cost_wvat>(?<=\n\€\n)[\d\,]+)[\s\S]+ODE[\s\S]{1}[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2}[\s\S]{3}'
    '(?P<ode_novat>(?<=\n\€\n)[\d\,]+)[\s\S]{3}'
    '(?P<ode_wvat>(?<=\n\€\n)[\d\,]+)\sVermindering energiebelasting\s[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2}[\s\S]{3}'
    '(?P<reduc_novat>(?<=\n\€\n)[\-\d\,]+)'
    '')

q = query.search(text)
print(q.group('present_period'))
# print(month)
# print(invoice_num)

#authorization
gc = pygsheets.authorize(service_file=GCREDS)

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('Utilities Dashboard')
# print(sh.sheets)

wks = sh.worksheet('title','Copy of '+ month)

wks.update_value('B4',q.group('present_period'))
print('sheets updated!')