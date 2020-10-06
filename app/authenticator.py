import jwt
import requests

keyset = requests.get('https://login.eveonline.com/oauth/jwks')


def validate_issuer(jwt):
    # https://docs.esi.evetech.net/docs/sso/validating_eve_jwt.html
    if jwt['iss'] not in (
            'login.eveonline.com', 'https://login.eveonline.com'):
        raise Exception('Unauthorized')


def get_jwt(event):
    key = [item for item in keyset['keys'] if item['alg'] == 'RS256'][0]
    return jwt.decode(event['authorizationToken'], key)


def policy_doc():
    return {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "Allow",
                    "Resource": "*"
                }
            ]
        }
    }


def handler(event, context):
    if 'authorizationToken' not in event:
        raise Exception('Unauthorized')
    # Figure out how to redirect on failed auth
    jwt = get_jwt(event)
    validate_issuer(jwt)
    return policy_doc()
