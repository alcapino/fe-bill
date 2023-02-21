from PyPDF2 import PdfReader
from settings import *
import pygsheets, re

month = 'FEB'

# Extract text.
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

# Find required values.
# Also used to check if the presented document is correct.
bill_values = re.search(BILL_QUERY,text)
if bill_values is None:
    print('Unrecognized document. Script will exit.')
    exit()

# Inconsistent positions
ean_el = re.search(EAN_ELECTRIC,text).group(0)
ean_gas = re.search(EAN_GAS,text).group(0)

# Inconsistent appearances
cover_extra_month = re.search(COVER_EXTRA,text)
refund_extra_month = re.search(REFUND_EXTRA,text)

# Checkpoint
print(f'Bill for {month} has been retrieved.\nGenerating report...')

gc = pygsheets.authorize(service_file=GCREDS)
sh = gc.open(GSPREADSHEET)
wks = sh.worksheet('title',f'Copy of {month}')

# Headers
wks.update_value('A1', f'Term invoice for {bill_values.group("month")}')
wks.update_value('B2',bill_values.group('invoice_num'))
wks.update_value('B3', bill_values.group('due_date'))
wks.update_value('B4',bill_values.group('present_period'))
wks.update_value('F2', bill_values.group('incl_BWT'))
wks.update_value('F3', bill_values.group('invoice_amt'))

# Fixed part
wks.update_values('E9:F12', [
    [bill_values.group('del_cost_novat'),bill_values.group('del_cost_wvat')],
    [bill_values.group('ode_novat'),bill_values.group('ode_wvat')],
    [bill_values.group('reduc_novat'),bill_values.group('reduc_wvat')],
    [bill_values.group('nmcost_novat'),bill_values.group('nmcost_wvat')],
])

# Dynamic part
# -- Gas
wks.update_values('C17:F18', [
    [
        bill_values.group('gas_consumption'),
        bill_values.group('gas_cons_ppu'),
        bill_values.group('gas_cons_novat'),
        bill_values.group('gas_cons_wvat'),
    ],
    [
        bill_values.group('gas_compensation'),
        bill_values.group('gas_comp_ppu'),
        bill_values.group('gas_comp_novat'),
        bill_values.group('gas_comp_wvat'),
    ],
])
# -- Electricity
wks.update_values('C20:F20', [[
    bill_values.group('el_consumption'),
    bill_values.group('el_cons_ppu'),
    bill_values.group('el_cons_novat'),
    bill_values.group('el_cons_wvat'),
]])

# VAT (BWT)
wks.update_values('F26:F28', [
    [bill_values.group('vat_0')],
    [bill_values.group('vat_9')],
    [bill_values.group('vat_21')],
])
# wks.update_value('C2', bill_values.group('____SAMPLE___'))

# Double term
# -- Covered
wks.update_value('B23', cover_extra_month.group('period') if cover_extra_month else 'X')
wks.update_value('E23', cover_extra_month.group('novat') if cover_extra_month else 'X')
wks.update_value('F23', cover_extra_month.group('wvat') if cover_extra_month else 'X')
# -- Refunded
wks.update_value('B24', refund_extra_month.group('period') if refund_extra_month else 'X')
wks.update_value('E24', refund_extra_month.group('novat') if refund_extra_month else 'X')
wks.update_value('F24', refund_extra_month.group('wvat') if refund_extra_month else 'X')

print(f'Sheet {month} updated!')