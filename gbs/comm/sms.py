import requests
import json
from gbs.conf import settings
API_ENDPOINT="https://www.my-cool-sms.com/api-socket.php"
HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

def send_sms(number, message):
    data = {'username': settings.SMS_USER, 
            'password': settings.SMS_PASS, 
            'function': 'sendSms',
            'number': number,
            'senderid': 'GrogBurners',
            'message': message
            }
    r = requests.post(API_ENDPOINT, data=json.dumps(data), headers=HEADERS)
    r.raise_for_status()
    return r.json()

