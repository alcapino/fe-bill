from PyPDF2 import PdfReader
from settings import DOCS_ROOT, GCREDS
import pygsheets, re
import pandas as pd


reader = PdfReader(DOCS_ROOT + "FEB.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()

# print(text)
# f = open("temp.txt", "w")
# f.write(text)
# f.close()
print("temp file written!")

month = re.search(r'(Termijnfactuur\s*)(\w*)', text).groups(1)
print(month)

#authorization
# gc = pygsheets.authorize(service_file=GCREDS)
gc = pygsheets.authorize(service_file=GCREDS)

# Create empty dataframe
df = pd.DataFrame()

# Create a column
df['name'] = ['John', 'Steve', 'Sarah']

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('PY to Gsheet Test')

#select the first sheet
wks = sh[0]

#update the first sheet with df, starting at cell B2.
wks.set_dataframe(df,(1,1))
print('sheets created!')