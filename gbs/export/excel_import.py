from openpyxl import load_workbook

def import_excel(filename):
    wb = load_workbook(filename)
    logger.debug(wb2.get_sheet_names())
