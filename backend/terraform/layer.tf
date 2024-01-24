module "generative_dependencies_layer" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lingolift-generative-deps-layer"
  description         = "Layer containing core dependencies like openai"
  compatible_runtimes = ["python3.11"]

  create_package = false
  local_existing_package = "../package_generative_deps.zip"
}
