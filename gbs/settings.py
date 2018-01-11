from django.apps import AppConfig

class GBSConfig(AppConfig):
    BIC = os.environ.get("BIC",'XXXXX')
    IBAN = os.environ.get("IBAN",'XXXXXXXXXXXXX')
