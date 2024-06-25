module "core_dependencies" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lingolift-core-dependencies-layer-${var.environment}"
  description         = "Core dependencies for non-NLP related tasks, including lingolift-shared and the OpenAI SDK"
  compatible_runtimes = ["python3.12"]


  create_package         = false
  local_existing_package = "../package_core_dependencies.zip"
}
