module "generative_dependencies_layer" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lingolift-generative-deps-layer"
  description         = "Layer containing core dependencies like openai"
  compatible_runtimes = ["python3.11"]

  source_path = "../package_generative"

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.generative_deps_layer.id
}

resource "aws_s3_bucket" "generative_deps_layer" {
    bucket = "lingolift-deps-layer-bucket"
}