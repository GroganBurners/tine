import unittest
import responses
from gbs.comm import sms


class SMSTest(unittest.TestCase):
    def setUp(self):
        responses.add(responses.POST, sms.API_ENDPOINT,
                      json={'success': True}, status=200)

    @responses.activate
    def test_sms_send(self):
        response = sms.send_sms("Hello, World!", "+353890000000")
        self.assertEqual(response['success'], True)
