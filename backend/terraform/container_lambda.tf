module "ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "syntactical_analysis-lambda"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [
    data.aws_caller_identity.current.arn,
    module.syntactical_analysis.lambda_role_arn
  ]

  repository_lifecycle_policy = local.repository_lifecycle_policy
}

module "syntactical_analysis" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "syntactical-analysis-lambda"
  description   = "Provides the /syntactical-analysis endpoint for the grammr application"

  create_package = false

  image_uri                    = "${module.ecr.repository_url}:latest"
  package_type                 = "Image"
  architectures                = ["x86_64"]

  memory_size = 2048
  timeout     = 15

  create_current_version_allowed_triggers = false
  allowed_triggers                        = local.allowed_triggers
  environment_variables = {
    "OPENAI_API_KEY" = var.openai_api_key
  }
}


locals {
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep 3 images",
        selection = {
          tagStatus   = "untagged",
          countType   = "imageCountMoreThan",
          countNumber = 2
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}

data "aws_caller_identity" "current" {}