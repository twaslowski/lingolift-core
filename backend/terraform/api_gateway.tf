resource "aws_api_gateway_rest_api" "lingolift_api" {
  name        = "lingolift_api"
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

resource "aws_api_gateway_stage" "dev" {
  depends_on = [aws_cloudwatch_log_group.logs]

  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  stage_name    = "v1"
}

resource "aws_cloudwatch_log_group" "logs" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.lingolift_api.id}/dev"
  retention_in_days = 14
}