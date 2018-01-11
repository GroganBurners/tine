from django.apps import AppConfig

class GBSConfig(AppConfig):
    BANK_ADDRESS = os.environ.get("BANK_ADDRESS",'Bank of Ireland, Parliament Street, Co. Kilkenny, R95 K857, Ireland')
    BIC = os.environ.get("BIC",'XXXXX')
    IBAN = os.environ.get("IBAN",'XXXXXXXXXXXXX')
    PHONE = os.environ.get("PHONE",'+353 87 634 1300')
    EMAIL_ADDR = os.environ.get("EMAIL_ADDR",'mick@groganburners.ie')
    REG_NO = os.environ.get("REG_NO",'451657')
    SORT_CODE = os.environ.get("SORT_CODE",'XX-XX-XX')
    VAT_NO = os.environ.get("VAT_NO",'IE 9675520W')
    WEBSITE = os.environ.get("WEBSITE",'https://www.groganburners.ie')
