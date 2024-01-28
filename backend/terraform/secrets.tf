resource "aws_secretsmanager_secret" "api_key" {
  name = "api-gateway/${var.environment}/api-key"
}

resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = aws_api_gateway_api_key.key.value
}

resource "aws_secretsmanager_secret" "stage_invoke_url" {
  name = "api-gateway/${var.environment}/base-url"
}

resource "aws_secretsmanager_secret_version" "api_base_url" {
  secret_id     = aws_secretsmanager_secret.stage_invoke_url.id
  secret_string = aws_api_gateway_stage.stage.invoke_url
}

resource "aws_secretsmanager_secret" "external_id" {
  name = "iam/${var.environment}/application-external-id"
}

resource "aws_secretsmanager_secret_version" "external_id" {
  secret_id = aws_secretsmanager_secret.external_id.id
  secret_string = random_password.external_id.result
}

resource "random_password" "external_id" {
  length = 32
}

resource "aws_iam_role" "client_role" {
  name = "ClientRole-${var.environment}"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "sts.amazonaws.com"
        }
        Condition = {
          "StringEquals" = {
            "sts:ExternalId" = aws_secretsmanager_secret_version.external_id.secret_string
          }
        }
      }
    ]
  })

  inline_policy {
    name = "ReadSecretPolicy-${var.environment}"

    policy = jsonencode({
      Version = "2012-10-17"
      Statement = [
        {
          Action   = ["secretsmanager:ReadSecretValue"]
          Effect   = "Allow"
          Resource = [aws_secretsmanager_secret.api_key.arn, aws_secretsmanager_secret.stage_invoke_url.arn]
        },
      ]
    })
  }
}