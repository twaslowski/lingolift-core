module "lambda_function_container_image" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.name}-lambda"
  description   = "Provides the translation endpoint for the grammr application"

  create_package = false
  timeout = 8

  image_uri    = "${module.ecr.repository_url}/${var.name}-lambda:latest"
  package_type = "Image"
  architectures = ["x86_64"]
  trigger_on_package_timestamp = true

  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}
