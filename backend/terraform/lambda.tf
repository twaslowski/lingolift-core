module "translation" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "translation-lambda"
  description   = "Provides the /translation endpoint for the grammr application"

  source_path = "../package_generative"
  handler     = "lambda_functions_generative.translation_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout = 5

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.code_bucket.id

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

module "literal_translation" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "literal-translation-lambda"
  description   = "Provides the /literal-translation endpoint for the grammr application"

  source_path = "../package_generative"
  handler     = "lambda_functions_generative.literal_translation_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout     = 10
  memory_size = 512

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.code_bucket.id

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

module "response_suggestion" {
  source        = "terraform-aws-modules/lambda/aws"
  function_name = "response-suggestion-lambda"
  description   = "Provides the /response-suggestion endpoint for the grammr application"

  source_path = "../package_generative"
  handler     = "lambda_functions_generative.response_suggestion_handler"

  runtime                      = "python3.11"
  architectures                = ["x86_64"]
  trigger_on_package_timestamp = true

  layers = [
    module.generative_dependencies_layer.lambda_layer_arn
  ]

  timeout     = 5
  memory_size = 256

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.code_bucket.id

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}

resource "aws_s3_bucket" "code_bucket" {
  bucket = "lingolift-lambdas-code-bucket"
}

variable "openai_api_key" {
  type = string
}