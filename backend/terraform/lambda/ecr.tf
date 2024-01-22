module "ecr" {
  source = "terraform-aws-modules/ecr/aws"

  repository_name                 = "${var.name}-lambda"
  repository_image_tag_mutability = "MUTABLE"

  repository_read_write_access_arns = [data.aws_caller_identity.current.arn]

  repository_lifecycle_policy = local.repository_lifecycle_policy
}

locals {
  repository_lifecycle_policy = jsonencode({
    rules = [
      {
        rulePriority = 1,
        description  = "Keep last 30 images",
        selection    = {
          tagStatus     = "tagged",
          tagPrefixList = ["v"],
          countType     = "imageCountMoreThan",
          countNumber   = 5
        },
        action = {
          type = "expire"
        }
      }
    ]
  })
}
