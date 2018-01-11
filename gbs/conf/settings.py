from django.conf import settings
import os

BANK_ADDRESS = getattr(settings, 'BANK_ADDRESS', os.environ.get("BANK_ADDRESS",'Bank of Ireland, Parliament Street, Co. Kilkenny, R95 K857, Ireland'))
BIC = getattr(settings, 'BIC', os.environ.get("BIC",'XXXXX'))
IBAN = getattr(settings, 'IBAN', os.environ.get("IBAN",'XXXXXXXXXXXXX'))
PHONE = getattr(settings, 'PHONE', os.environ.get("PHONE",'+353 87 634 1300'))
EMAIL = getattr(settings, 'EMAIL_ADDR', os.environ.get("EMAIL_ADDR",'mick@groganburners.ie'))
REG_NO = getattr(settings, 'REG_NO', os.environ.get("REG_NO",'451657'))
SORT_CODE = getattr(settings, 'SORT_CODE', os.environ.get("SORT_CODE",'XX-XX-XX'))
VAT_NO = getattr(settings, 'VAT_NO', os.environ.get("VAT_NO",'IE 9675520W'))
WEBSITE = getattr(settings, 'WEBSITE', os.environ.get("WEBSITE",'https://www.groganburners.ie'))
