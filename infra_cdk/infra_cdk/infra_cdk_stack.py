import os, sys
import random
import string 
import json
import shutil
from constructs import Construct

from aws_cdk import (
    Duration,
    Stack,
    RemovalPolicy,
    SecretValue as secretvalue,
    aws_lambda as _lambda, 
    aws_apigatewayv2_alpha as apigateway,
    aws_secretsmanager as secrets, 
    aws_iam as iam
) 

# dir
dir = os.path.dirname(__file__)
# parent  dir
root_dir = os.path.dirname(os.path.dirname(dir))
abs_path = os.path.abspath(dir)
rand = '-'+ ''.join(random.choice(string.ascii_lowercase) for i in range(4))
 
from aws_cdk.aws_apigatewayv2_integrations_alpha import HttpLambdaIntegration
from aws_cdk.aws_apigatewayv2_authorizers_alpha import (
    HttpLambdaAuthorizer,
    HttpLambdaResponseType,
)
 

class InfraCdkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create apigateway
        api_name = "preferred_item_service-api"
        preferred_item_service_api = apigateway.HttpApi(self, api_name) 
        code_path = os.path.join(root_dir, "preferred_item_service")
 
        bundling_dependencies(code_path)
        lambda_code = _lambda.Code.from_asset(f'{abs_path}/asset-output{rand}.zip')
        # create secret for authorization
        secret_name = "Authorization_Key"
        auth_secret = secrets.Secret(
            self,
            "authorization-token",
            secret_name=secret_name,
            secret_object_value={
                "auth-token": secretvalue.unsafe_plain_text(
                    "".join(
                        random.choices(
                            string.ascii_uppercase + string.ascii_lowercase, k=16
                        )
                    )
                )
            },
        )
        # api_code = _lambda.Code.from_inline(
        #     open(
        #         os.path.join(root_dir, "preferred_item_service//api//main.py"), "r"
        #     ).read()
        # )
        api_authorizer_code = _lambda.Code.from_inline(
            open(os.path.join(dir, "api_auth.py"), "r").read()
        )

        preferred_item_service = create_lambda(
            self,
            "preferred_item_service",
            "preferred_item_service.api.main.handler",
            " AWS Lambda API for preferred_item_service",
            lambda_code,
            "CreateLambdaPreferredItemService",
        )

        # preferred_item_service = PythonFunction(self, "function",
        #     entry=os.path.join(root_dir, "preferred_item_service"),
        #     index=os.path.join(root_dir, "preferred_item_service//api//main.py"),
        #     runtime= _lambda.Runtime.PYTHON_3_9,
        #     handler="preferred_item_service.api.main.handler"
        #   )

        api_authorizer_lambda = create_lambda(
            self,
            "api_authorizer_lambda",
            "index.lambda_handler",
            "AWS Lambda API for authorizing api",
            api_authorizer_code,
            "CreateLambdaAuthorizor",
            env={"secret_arn": auth_secret.secret_arn},
        )
        
        authorizer = HttpLambdaAuthorizer(
            "apiAuthorizer",
            api_authorizer_lambda,
            response_types=[HttpLambdaResponseType.SIMPLE],
        )

        # create http route for api gateway
        docs_route = apigateway.HttpRoute(
            self,
            "docs_route",
            http_api=preferred_item_service_api,
            integration=HttpLambdaIntegration(
                id="preferred_item_service",
                handler=preferred_item_service,
            ),
            route_key=apigateway.HttpRouteKey.with_(
                "/docs", apigateway.HttpMethod.ANY
            ),
             
        )
        
                # create http route for api gateway
        api_route = apigateway.HttpRoute(
            self,
            "api_route",
            http_api=preferred_item_service_api,
            integration=HttpLambdaIntegration(
                id="preferred_item_service",
                handler=preferred_item_service,
            ),
            route_key=apigateway.HttpRouteKey.with_(
                "/openapi.json", apigateway.HttpMethod.ANY
            ), 
        )
        proxy_route = apigateway.HttpRoute(
            self,
            "proxy_route",
            http_api=preferred_item_service_api,
            integration=HttpLambdaIntegration(
                id="preferred_item_service",
                handler=preferred_item_service,
            ),
            route_key=apigateway.HttpRouteKey.with_(
                "/{proxy+}", apigateway.HttpMethod.ANY
            ),
            authorizer=authorizer,
        )

def create_lambda(
    cls: classmethod,
    function_name,
    handler,
    desc,
    code,
    stack_id="CreateLambda",
    env={},
):
    return _lambda.Function(
        cls,
        stack_id,
        function_name=function_name,
        runtime=_lambda.Runtime.PYTHON_3_9,
        handler=handler,
        timeout=Duration.minutes(10),
        description=desc,
        tracing=_lambda.Tracing.ACTIVE,
        environment=env,
        code=code,
    )
def bundling_dependencies(code_path):
    shutil.copytree(code_path, f'{abs_path}/asset-output')
    os.system(
        f'pip install --upgrade -r {code_path}/requirements.txt -t {abs_path}/asset-output')
    shutil.make_archive(f'{abs_path}/asset-output{rand}',
                        'zip', f'{abs_path}/asset-output')
    shutil.rmtree(f'{abs_path}/asset-output')