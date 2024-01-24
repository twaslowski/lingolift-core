module "generative_dependencies_layer" {
  source = "terraform-aws-modules/lambda/aws"

  create_layer = true

  layer_name          = "lingolift-generative-deps-layer"
  description         = "Dependency layer"
  compatible_runtimes = ["python3.11"]

  source_path = "../package_generative_deps"

  store_on_s3 = true
  s3_bucket   = aws_s3_bucket.generative_deps_layer.id
}

#module "nlp_dependencies_layer" {
#  source = "terraform-aws-modules/lambda/aws"
#
#  create_layer = true
#
#  layer_name          = "lingolift-nlp-deps-layer"
#  description         = "Dependency layer"
#  compatible_runtimes = ["python3.11"]
#
#  source_path = "../package_nlp_deps"
#
#  store_on_s3 = true
#  s3_bucket   = aws_s3_bucket.generative_deps_layer.id
#}

resource "aws_s3_bucket" "generative_deps_layer" {
    bucket = "lingolift-deps-layer-bucket"
}