resource "aws_secretsmanager_secret" "api_key" {
  name = "api-gateway/${var.environment}/api-key"
}

resource "aws_secretsmanager_secret_version" "api_key" {
  secret_id     = aws_secretsmanager_secret.api_key.id
  secret_string = aws_api_gateway_api_key.key.value
}

resource "aws_secretsmanager_secret" "api_url" {
  name = "api-gateway/${var.environment}/base-url"
}

resource "aws_secretsmanager_secret_version" "api_base_url" {
  secret_id     = aws_secretsmanager_secret.api_url.id
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