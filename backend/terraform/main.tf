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

module "response_suggestion-lambda" {
  source         = "./lambda"
  openai_api_key = var.openai_api_key
  name           = "response_suggestion"
}
variable "openai_api_key" {
  type = string
}