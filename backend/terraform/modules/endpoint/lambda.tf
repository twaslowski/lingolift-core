module "lambda" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "${var.name}-lambda"
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

  layers = var.layers

  timeout          = var.timeout
  allowed_triggers = local.allowed_triggers

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
