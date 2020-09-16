#!/usr/bin/env python3

from aws_cdk import core

from cdk_app.cdk_app_stack import CdkAppStack


app = core.App()
CdkAppStack(app, "cdk-app")

app.synth()
