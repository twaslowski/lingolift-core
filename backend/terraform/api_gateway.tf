resource "aws_api_gateway_rest_api" "lingolift_api" {
  name        = "lingolift_api_${var.environment}"
  description = "The Lingolift API"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id

  triggers = {
    redeployment = join("", [
      filesha1("api_gateway.tf"),
      filesha1("lambda.tf"),
    ])
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "stage" {
  depends_on = [aws_cloudwatch_log_group.logs]

  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  stage_name    = var.environment
}

resource "aws_cloudwatch_log_group" "logs" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.lingolift_api.id}/${var.environment}"
  retention_in_days = 14
}

resource "aws_api_gateway_account" "api_gateway_account" {
  # There should only be one of these per region per account, so only create it in dev
  # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
  count = var.environment == "dev" ? 1 : 0

  cloudwatch_role_arn = aws_iam_role.cloudwatch.arn
}

resource "aws_iam_role" "cloudwatch" {
  # There should only be one of these per region per account, so only create it in dev
  # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-apigateway-account.html
  name = "api_gateway_cloudwatch_global"

  assume_role_policy = jsonencode({
    Version   = "2012-10-17"
    Statement = [
      {
        Action    = "sts:AssumeRole"
        Effect    = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })
  managed_policy_arns = ["arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"]
}