module "translation-lambda" {
  source = "./lambda"
  openai_api_key = var.openai_api_key
  name = "translation"
}

module "translation-lambda" {
  source = "./lambda"
  openai_api_key = var.openai_api_key
  name = "literal-translation"
}

module "translation-lambda" {
  source = "./lambda"
  openai_api_key = var.openai_api_key
  name = "response-suggestion"
}
variable "openai_api_key" {
  type = string
}