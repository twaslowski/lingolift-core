module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "${var.name}-lambda-${var.environment}"
  description   = "Provides the /${var.name} endpoint for the grammr application"

  create_package                          = false
  create_current_version_allowed_triggers = false
  package_type                            = var.package_type
  trigger_on_package_timestamp            = true
  runtime                                 = var.runtime
  architectures                           = ["x86_64"]
  handler                                 = var.handler

  local_existing_package = var.local_existing_package
  image_uri              = var.image_uri
  memory_size            = var.memory

  layers                            = var.layers
  cloudwatch_logs_retention_in_days = 14

  timeout          = var.timeout
  allowed_triggers = local.allowed_triggers

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

resource "aws_cloudwatch_event_rule" "keep_warm" {
  # These are only required on the much slower container-based lambdas
  count = var.package_type == "Image" ? 1 : 0

  name                = "every-ten-minutes"
  description         = "Fires every ten minutes"
  schedule_expression = "rate(10 minutes)"
}

resource "aws_cloudwatch_event_target" "keep_warm" {
  count = var.package_type == "Image" ? 1 : 0

  rule      = aws_cloudwatch_event_rule.keep_warm[0].name
  target_id = "${module.lambda.lambda_function_name}-keep-warm"
  arn       = module.lambda.lambda_function_arn

  input_transformer {
    input_template = <<JSON
    {
      "body": "{\"pre_warm\": \"true\"}"
    }
  JSON
  }
}

locals {
  allowed_triggers = {
    apigateway = {
      service    = "apigateway"
      source_arn = "arn:aws:execute-api:eu-central-1:${data.aws_caller_identity.current.account_id}:*"
    },
    eventbridge = {
      service    = "events"
      source_arn = "arn:aws:events:eu-central-1:${data.aws_caller_identity.current.account_id}:rule/*"
    }
  }
}
