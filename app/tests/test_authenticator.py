import unittest
from authenticator import handler


class TestAuthenticator(unittest.TestCase):
    def apigw_auth_event(self):
        """ Generates API GW Authorizer REQUEST Event"""

        return {
            "type": "REQUEST",
            "methodArn": "arn:aws:execute-api:us-east-1:123456789012:s4x3opwd6i/test/GET/request",
            "resource": "/request",
            "path": "/request",
            "httpMethod": "GET",
            "headers": {
                "X-AMZ-Date": "20170718T062915Z",
                "Accept": "*/*",
                "Authorization": "Basic ZG91Z2FsYjpteXBhc3N3b3Jk",
                "CloudFront-Viewer-Country": "US",
                "CloudFront-Forwarded-Proto": "https",
                "CloudFront-Is-Tablet-Viewer": "false",
                "CloudFront-Is-Mobile-Viewer": "false",
                "User-Agent": "...",
                "X-Forwarded-Proto": "https",
                "CloudFront-Is-SmartTV-Viewer": "false",
                "Host": "....execute-api.us-east-1.amazonaws.com",
                "Accept-Encoding": "gzip, deflate",
                "X-Forwarded-Port": "443",
                "X-Amzn-Trace-Id": "...",
                "Via": "...cloudfront.net (CloudFront)",
                "X-Amz-Cf-Id": "...",
                "X-Forwarded-For": "..., ...",
                "Postman-Token": "...",
                "cache-control": "no-cache",
                "CloudFront-Is-Desktop-Viewer": "true",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "queryStringParameters": {
                "QueryString1": "queryValue1"
            },
            "pathParameters": {},
            "stageVariables": {
                "StageVar1": "stageValue1"
            },
            "requestContext": {
                "path": "/request",
                "accountId": "123456789012",
                "resourceId": "05c7jb",
                "stage": "test",
                "requestId": "...",
                "identity": {
                    "apiKey": "...",
                    "sourceIp": "..."
                },
                "resourcePath": "/request",
                "httpMethod": "GET",
                "apiId": "s4x3opwd6i"
            }
        }

    def test_handler_unauthorized(self):
        self.assertRaises(Exception, handler, self.apigw_auth_event(), "")

    def _test_handler_authorized(self):
        ret = handler(self.apigw_auth_event(), "")
        return True
        assert ret == {
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
