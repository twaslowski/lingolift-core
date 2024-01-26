module "translation" {
  source                 = "./modules/endpoint"
  api_gateway_id         = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id       = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  runtime                = "python3.11"
  name                   = "translation"
  local_existing_package = "../package_generative.zip"
  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]
  handler        = "lambda_functions_generative.translation_handler"
  openai_api_key = var.openai_api_key
}

module "literal_translation" {
  source                 = "./modules/endpoint"
  api_gateway_id         = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id       = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  runtime                = "python3.11"
  name                   = "literal-translation"
  local_existing_package = "../package_generative.zip"
  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]
  handler        = "lambda_functions_generative.literal_translation_handler"
  openai_api_key = var.openai_api_key
}

module "response_suggestion" {
  source           = "./modules/endpoint"
  api_gateway_id   = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id = aws_api_gateway_rest_api.lingolift_api.root_resource_id

  runtime                = "python3.11"
  name                   = "response-suggestion"
  local_existing_package = "../package_generative.zip"
  memory                 = 2048
  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]
  handler        = "lambda_functions_generative.response_suggestion_handler"
  openai_api_key = var.openai_api_key
}

module "syntactical_analysis" {
  source           = "./modules/endpoint"
  api_gateway_id   = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id = aws_api_gateway_rest_api.lingolift_api.root_resource_id

  name         = "syntactical-analysis"
  package_type = "Image"
  image_uri    = "${module.ecr.repository_url}:latest"

  memory = 2048

  handler        = "lambda_functions_generative.response_suggestion_handler"
  openai_api_key = var.openai_api_key
}


variable "openai_api_key" {
  type = string
}

locals {
  allowed_triggers = {
    apigateway = {
      service    = "apigateway"
      source_arn = "arn:aws:execute-api:eu-central-1:246770851643:*"
    }
  }
}