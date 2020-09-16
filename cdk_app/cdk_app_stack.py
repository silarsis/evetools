from aws_cdk import (
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_route53 as route53,
    core
)

domain_name = 'eve.bofh.net.au'


class CdkAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        zone = route53.PublicHostedZone(
            self, "HostedZone", zone_name=domain_name)

        s3_hname = "www"

        bucket = s3.Bucket(
            self, "KJLEveToolsBucket",
            bucket_name=".".join([s3_hname, domain_name]),
            public_read_access=True,
            website_index_document="index.html",
            versioned=True)

        hello_lambda = _lambda.Function(
            self, 'HelloHandler', runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.asset('hello'),
            handler='hello.handler'
        )

        rest_api = apigw.LambdaRestApi(
            self, 'Endpoint',
            handler=hello_lambda
        )

        # route53.ARecord(
        #     self, "AliasRecord", zone=zone,
        #     target=route53.RecordTarget(rest_api))

        # Also an A record for the S3 bucket