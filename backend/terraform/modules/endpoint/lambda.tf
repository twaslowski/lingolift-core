module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "${var.name}-lambda"
  description   = "Provides the /${var.name} endpoint for the grammr application"

  create_package         = false
  local_existing_package = var.local_existing_package
  package_type           = var.package_type
  handler                = var.handler

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = var.layers

  timeout                                 = var.timeout
  create_current_version_allowed_triggers = false
  allowed_triggers                        = local.allowed_triggers

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

locals {
  allowed_triggers = {
    apigateway = {
      service    = "apigateway"
      source_arn = "arn:aws:execute-api:eu-central-1:246770851643:*"
    }
  }
}
