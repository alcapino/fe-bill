from PyPDF2 import PdfReader
from settings import *
import pygsheets, re

month = 'FEB'
reader = PdfReader(f'{DOCS_ROOT}{month}.pdf')
number_of_pages = len(reader.pages)
text = ''
for i in range(number_of_pages):
    page = reader.pages[i]
    text += page.extract_text()

# # print(text)
# f = open("temp.txt", "w")
# f.write(text)
# f.close()
# print("temp file written!")


ean_el = re.search(EAN_ELECTRIC,text).group(0)
ean_gas = re.search(EAN_GAS,text).group(0)
cover_extra_month = re.search(COVER_EXTRA,text)
refund_extra_month = re.search(REFUND_EXTRA,text)
bill_values = re.search(BILL_QUERY,text)
print(f'Bill for {month} has been retrieved. Generating report...')

gc = pygsheets.authorize(service_file=GCREDS)
sh = gc.open(GSPREADSHEET)
# print(sh.sheets)

wks = sh.worksheet('title',f'Copy of {month}')
if bill_values is not None:
    wks.update_value('B2',bill_values.group('invoice_num'))
    wks.update_value('B3', bill_values.group('due_date'))
    wks.update_value('B4',bill_values.group('present_period'))
    wks.update_value('F2', bill_values.group('incl_BWT'))
    wks.update_value('F3', bill_values.group('invoice_amt'))
    # wks.update_value('B2', bill_values.group('____SAMPLE___'))
    # wks.update_value('B2', bill_values.group('____SAMPLE___'))
else:
    print('Unrecognized document. Script will exit.')
    exit()
print(f'Sheet {month} updated!')