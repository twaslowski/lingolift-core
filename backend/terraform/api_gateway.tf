module "api_gateway" {
  source = "terraform-aws-modules/apigateway-v2/aws"

  name                 = "lingolift-api"
  description          = "The Lingolift API"
  protocol_type        = "HTTP"
  create_default_stage = true

  cors_configuration = {
    allow_headers = [
      "content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"
    ]
    allow_methods = ["POST", "GET"]
    allow_origins = ["*"]
  }

  default_stage_access_log_destination_arn = aws_cloudwatch_log_group.logs.arn
  default_stage_access_log_format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId $context.integrationErrorMessage"

  default_route_settings = {
    detailed_metrics_enabled = true
    throttling_burst_limit   = 100
    throttling_rate_limit    = 100
  }

  integrations = {
    "POST /translation" = {
      lambda_arn             = module.translation-lambda.lambda_function_arn
      payload_format_version = "2.0"
      timeout_milliseconds   = 15000
    }
  }
}

resource "aws_cloudwatch_log_group" "logs" {
  name = "/aws/apigateway/lingolift-api"
}