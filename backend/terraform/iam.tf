resource "aws_iam_role" "external_role" {
  name = "read-secrets-manager"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Action    = "sts:AssumeRole"
        Principal = {
          Service = "sts.amazonaws.com"
        }
        Condition = {
          StringEquals = {
            Test = "StringEquals"
            Variable = "sts:ExternalId"
            Values = aws_secretsmanager_secret_version.external_id.secret_string
          }
        }
      }
    ]
  })
}

resource "aws_s3_bucket_policy" "allow_secrets_manager" {
  bucket = "example-bucket"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": aws_iam_role.external_role.arn
        },
        "Action": [
          "secretsmanager:GetSecretValue",
        ],
        "Resource": [
          aws_secretsmanager_secret.api_url.arn,
          aws_secretsmanager_secret.api_key.arn
        ]
      }
    ]
  })
}

