import json
import jwt
import requests
from urllib.parse import urlencode

class BubblecheckCognito:
    cognito_url = ""
    cognito_client_id = ""

    def init_app(self, app):
        self.cognito_url = app.config['COGNITO_URL']
        self.cognito_client_id = app.config['COGNITO_CLIENT_ID']

    def get_email_from_code(self, code, callback_url):
        code_exchange_url = "https://{}/oauth2/token".format(self.cognito_url)
        payload = {
            'grant_type'   : 'authorization_code',
            'code'         : code,
            'client_id'    : self.cognito_client_id,
            'redirect_uri' : callback_url
        }
        response = requests.request('POST', code_exchange_url, data=payload)
        # We do *not* verify this JWT, because we just got it from AWS can can therefore trust it.
        jwt_token = json.loads(response.text).get('id_token')
        if not jwt_token:
            return None
        decoded_jwt = jwt.decode(jwt_token, verify=False)
        return decoded_jwt.get('email')

    def cognito_login_url(self, callback_url):
        parameters = {
            'client_id': self.cognito_client_id,
            'redirect_uri': callback_url,
            'response_type': 'code'
        }
        return 'https://{}/login?{}'.format(
            self.cognito_url,
            urlencode(parameters)
        )
        
cognito = BubblecheckCognito()