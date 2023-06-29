import os
import requests
import hmac
from hashlib import sha1
from time import time
from dotenv import load_dotenv
import json
from pprint import pprint


class SILApi:
    def __init__(self):
        load_dotenv()
        self.limit = 5

    def load_language_details(self):
        api_url = 'https://progressbible-language-v1.apis.sil.org/'
        api_key = os.getenv('PB_LD_KEY')
        api_secret = os.getenv('PB_LD_SECRET')

        return self._load_data(api_url, api_key, api_secret)

    def load_language_and_dialects(self):
        api_url = 'https://progressbible-l-d-ic-v1.apis.sil.org/'
        api_key = os.getenv('PB_LDIC_KEY')
        api_secret = os.getenv('PB_LDIC_SECRET')

        return self._load_data(api_url, api_key, api_secret)

    def load_uw_language_details(self):
        api_url = 'https://unfoldingword-language-detail-v1.apis.sil.org/'
        api_key = os.getenv('UW_LD_KEY')
        api_secret = os.getenv('UW_LD_SECRET')

        return self._load_data(api_url, api_key, api_secret)

    def _load_data(self, api_url, api_key, api_secret):
        api_sig = self._get_api_sig(api_key, api_secret)
        full_url = api_url + '?api_key=' + api_key + '&api_sig=' + api_sig + '&limit=' + str(self.limit)

        content = requests.get(full_url, verify=False).content
        return json.loads(content)

    def _get_api_sig(self, key, secret):
        curr_time = str(int(time()))
        base_val = curr_time + key
        # hmac expects byte, python 3.x requires explicit conversion
        base_val_b = base_val.encode('utf-8')
        secret_b = secret.encode('utf-8')
        h1 = hmac.new(secret_b, base_val_b, sha1)
        # h1 is byte, so convert to hex
        api_sig = h1.hexdigest()

        return api_sig


silapi = SILApi

lang_details = silapi.load_language_details(SILApi())
pprint(lang_details)

#print(silapi.load_language_and_dialects(SILApi()))
#print(silapi.load_uw_language_details(SILApi()))
