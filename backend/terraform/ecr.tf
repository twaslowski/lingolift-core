moved {
  from = module.ecr
  to   = module.syntactical_analysis_repository
}

module "syntactical_analysis_repository" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "syntactical_analysis-lambda-${var.environment}"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [
    data.aws_caller_identity.current.arn,
    module.syntactical_analysis.lambda_role_arn
  ]

  repository_lifecycle_policy = local.repository_lifecycle_policy
}

module "inflection_repository" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "inflection-lambda-${var.environment}"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [
    data.aws_caller_identity.current.arn,
    module.syntactical_analysis.lambda_role_arn
  ]

  repository_lifecycle_policy = local.repository_lifecycle_policy
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