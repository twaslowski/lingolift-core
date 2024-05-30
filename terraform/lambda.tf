module "translation" {
  source                 = "./modules/endpoint"
  environment      = var.environment
  api_gateway_id         = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id       = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  runtime                = "python3.11"
  name                   = "translation"
  local_existing_package = "../package_core.zip"
  layers                 = [
    module.core_dependencies.lambda_layer_arn
  ]
  handler        = "lambda_handlers.translation_handler"
  openai_api_key = var.openai_api_key
}

module "literal_translation" {
  source                 = "./modules/endpoint"
  environment      = var.environment
  api_gateway_id         = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id       = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  runtime                = "python3.11"
  name                   = "literal-translation"
  local_existing_package = "../package_core.zip"
  layers                 = [
    module.core_dependencies.lambda_layer_arn
  ]
  handler        = "lambda_handlers.literal_translation_handler"
  openai_api_key = var.openai_api_key
}

module "response_suggestion" {
  source           = "./modules/endpoint"
  environment      = var.environment
  api_gateway_id   = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id = aws_api_gateway_rest_api.lingolift_api.root_resource_id

  runtime                = "python3.11"
  name                   = "response-suggestion"
  local_existing_package = "../package_core.zip"
  layers                 = [
    module.core_dependencies.lambda_layer_arn
  ]
  handler        = "lambda_handlers.response_suggestion_handler"
  openai_api_key = var.openai_api_key
}

module "syntactical_analysis" {
  source           = "./modules/endpoint"
  environment      = var.environment
  api_gateway_id   = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id = aws_api_gateway_rest_api.lingolift_api.root_resource_id

  name         = "syntactical-analysis"
  package_type = "Image"
  image_uri    = "${module.syntactical_analysis_repository.repository_url}:sha-${var.commit_sha}"

  memory = 2048

  openai_api_key = var.openai_api_key
}

module "inflection" {
  source           = "./modules/endpoint"
  environment      = var.environment
  api_gateway_id   = aws_api_gateway_rest_api.lingolift_api.id
  root_resource_id = aws_api_gateway_rest_api.lingolift_api.root_resource_id

  name         = "inflection"
  package_type = "Image"
  image_uri    = "${module.inflection_repository.repository_url}:sha-${var.commit_sha}"

  memory = 2048

  openai_api_key = var.openai_api_key
}
