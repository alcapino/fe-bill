from PyPDF2 import PdfReader
from settings import *
import pygsheets, re

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

query = re.compile("".join(BILL_QUERY))

q = query.search(text)
print(q.group('present_period'))
# print(month)
# print(invoice_num)

gc = pygsheets.authorize(service_file=GCREDS)
sh = gc.open(GSPREADSHEET)
# print(sh.sheets)

wks = sh.worksheet('title','Copy of '+ month)

wks.update_value('B4',q.group('present_period'))
print('sheets updated!')