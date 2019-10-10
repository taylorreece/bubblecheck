import json
import jwt
import requests

class BubblecheckCognito:
    cognito_uri = ""
    cognito_client_id = ""

    def init_app(self, app):
        self.cognito_uri = app.config['COGNITO_URI']
        self.cognito_client_id = app.config['COGNITO_CLIENT_ID']

    def get_email_from_code(self, code, host):
        code_exchange_url = "https://{}/oauth2/token".format(self.cognito_uri)
        payload = {
            'grant_type'   : 'authorization_code',
            'code'         : code,
            'client_id'    : self.cognito_client_id,
            'redirect_uri' : 'http://{}/api/user/oauth/cognito_callback'.format(host)
        }
        response = requests.request('POST', code_exchange_url, data=payload)
        # We do *not* verify this JWT, because we just got it from AWS can can therefore trust it.
        jwt_token = json.loads(response.text).get('id_token')
        decoded_jwt = jwt.decode(jwt_token, verify=False)
        return decoded_jwt.get('email')

cognito = BubblecheckCognito()