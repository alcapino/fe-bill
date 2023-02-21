DOCS_ROOT = '../docs/'
GCREDS = './creds.json'
GSPREADSHEET = 'Utilities Dashboard'
EAN_ELECTRIC = r'(?P<EAN_el>(?<=\nEAN[\W]{2}elektriciteit\n:\n)[\d]+)'
EAN_GAS = r'(?P<EAN_gas>(?<=\nEAN[\W]{2}gas\n:\n)[\d]+)'
COVER_EXTRA = r'Dekking extra maand\n' \
              r'(?P<cover_extra_period>[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2})[\W]{3}' \
              r'(?P<cover_extra_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
              r'(?P<cover_extra_wvat>(?<=€\n)[\d\,]+)'
REFUND_EXTRA = r'Restitutie extra maand\n' \
              r'(?P<refund_extra_period>[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2})[\W]{3}' \
              r'(?P<refund_extra_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
              r'(?P<refund_extra_wvat>(?<=€\n)[\d\,]+)'
BILL_QUERY = r'Klantnummer:\n' \
    r'(?P<customer_num>\d+)\nFactuurnummer:\n' \
    r'(?P<invoice_num>\d+)\nVervaldatum:\n' \
    r'(?P<due_date>[\d\-]+)[\s\S]+Termijnfactuur\s{3}' \
    r'(?P<month>\w*)[\s\S]+Vaste leveringskosten\n' \
    r'(?P<present_period>[\d]{2}\-[\d]{2} t\/m [\d]{2}\-[\d]{2})[\W]{3}' \
    r'(?P<del_cost_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
    r'(?P<del_cost_wvat>(?<=€\n)[\d\,]+)[\s\S]+ODE[\w\s\-\/]+[\W]{3}' \
    r'(?P<ode_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
    r'(?P<ode_wvat>(?<=€\n)[\d\,]+)\nVermindering energiebelasting[\w\s\-\/]+[\W]{3}' \
    r'(?P<reduc_novat>(?<=€\n)[\-\d\,]+)[\W]{3}' \
    r'(?P<reduc_wvat>(?<=€\n)[\-\d\,]+)\nNetbeheerkosten[\w\s\-\/]+[\W]{2}' \
    r'(?P<nmcost_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
    r'(?P<nmcost_wvat>(?<=€\n)[\-\d\,]+)[\s\S]+verbruik[\w\s\-\/]+\n' \
    r'(?P<gas_consumption>\d+)[\W]{3}m[\s\S]{5}' \
    r'(?P<gas_cons_ppu>(?<=€\n)[\-\d\,]+)\W{3}' \
    r'(?P<gas_cons_novat>(?<=€\n)[\d\,]+)\W{3}' \
    r'(?P<gas_cons_wvat>(?<=€\n)[\d\,]+)[\s\S]+compensatie[\w\s\-\/]+\n' \
    r'(?P<gas_compensation>\d+)[\W]{3}m[\s\S]{5}' \
    r'(?P<gas_comp_ppu>(?<=€\n)[\-\d\,]+)\W{3}' \
    r'(?P<gas_comp_novat>(?<=€\n)[\-\d\,]+)\W{3}' \
    r'(?P<gas_comp_wvat>(?<=€\n)[\-\d\,]+)\nLeveringsadres:\n' \
    r'(?P<delivery_add>[\w \,\d]+)[\s\S]+' \
    r'(?P<incl_BWT>(?<=Incl\.[\W]{2})[\d\,]+)[\W]{2}BTW[\W]{3}' \
    r'(?P<invoice_amt>(?<=€\n)[\d\,]+)[\s\S]+verbruik[\w\s\-\/]+\n' \
    r'(?P<el_consumption>\d+)[\W]{3}kWh[\W]{3}' \
    r'(?P<el_cons_ppu>(?<=€\n)[\-\d\,]+)[\W]{3}' \
    r'(?P<el_cons_novat>(?<=€\n)[\d\,]+)[\W]{3}' \
    r'(?P<el_cons_wvat>(?<=€\n)[\d\,]+)[\s\S]+[\s\S]+0\n\%[\W]{3}' \
    r'(?P<vat_0>(?<=€\n)[\-\d\,]+)[\s\S]+9\n\%[\W]{3}' \
    r'(?P<vat_9>(?<=€\n)[\-\d\,]+)[\s\S]+21\n\%[\W]{3}' \
    r'(?P<vat_21>(?<=€\n)[\-\d\,]+)'