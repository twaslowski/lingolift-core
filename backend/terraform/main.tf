module "translation-lambda" {
  source         = "./lambda"
  openai_api_key = var.openai_api_key
  name           = "translation"
}

module "literal_translation-lambda" {
  source         = "./lambda"
  openai_api_key = var.openai_api_key
  name           = "literal_translation"
}

module "syntactical_analysis-lambda" {
  source         = "./lambda"
  openai_api_key = "not-needed"
  name           = "syntactical_analysis"

  memory_size = 1024
  timeout     = 30
}

module "response_suggestion-lambda" {
  source         = "./lambda"
  openai_api_key = var.openai_api_key
  name           = "response_suggestion"
}
variable "openai_api_key" {
  type = string
}