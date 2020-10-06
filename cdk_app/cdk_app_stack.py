from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_route53 as route53,
    aws_certificatemanager as acm,
    core
)

DOMAIN_NAME = 'eve.bofh.net.au'
S3_HOSTNAME = "www"
API_HOSTNAME = 'api'
RUNTIME = _lambda.Runtime.PYTHON_3_7


class CdkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        hosted_zone = route53.PublicHostedZone(
            self, "HostedZone",
            zone_name=DOMAIN_NAME
        )

        certificate = acm.Certificate(
            self, 'Certificate',
            domain_name='.'.join(['*', DOMAIN_NAME]),
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        dns_options = apigw.DomainNameOptions(
            domain_name='.'.join([API_HOSTNAME, DOMAIN_NAME]),
            certificate=certificate
        )

        s3.Bucket(
            self, "KJLEveToolsBucket",
            bucket_name=".".join([S3_HOSTNAME, DOMAIN_NAME]),
            public_read_access=True,
            website_index_document="index.html",
            versioned=True
        )

        hello_lambda = _lambda.Function(
            self, 'HelloHandler', runtime=RUNTIME,
            code=_lambda.Code.asset('app'),
            handler='hello.handler'
        )

        authenticator_lambda = _lambda.Function(
            self, 'AuthenticatorHandler', runtime=RUNTIME,
            code=_lambda.Code.asset('app'),
            handler='authenticator.handler'
        )

        authorizer = apigw.TokenAuthorizer(
            self, 'EveOAuth',
            handler=authenticator_lambda
        )

        apigw.LambdaRestApi(
            self, 'EveTools',
            domain_name=dns_options,
            handler=hello_lambda,
            default_method_options={'authorizer': authorizer}
        )

        # route53.ARecord(
        #     self, "AliasRecord", zone=zone,
        #     target=route53.RecordTarget(rest_api))

        # Also an A record for the S3 bucket

        # OAuth callback
        # https://api.eve.bofh.net.au/auth-callback
