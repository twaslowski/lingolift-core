resource "aws_secretsmanager_secret" "api_key" {
  name = "api-gateway/${var.environment}/api-key"
}

resource "aws_secretsmanager_secret_version" "example" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = aws_api_gateway_api_key.key.value
}

resource "aws_secretsmanager_secret" "api_url" {
  name = "api-gateway/${var.environment}/base-url"
}

resource "aws_secretsmanager_secret_version" "example" {
  secret_id     = aws_secretsmanager_secret.api_url.id
  secret_string = aws_api_gateway_stage.stage.invoke_url
}