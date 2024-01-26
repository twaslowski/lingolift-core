resource "aws_api_gateway_rest_api" "lingolift_api" {
  name        = "lingolift_api"
  description = "The Lingolift API"
}

resource "aws_api_gateway_resource" "syntactical_analysis" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id
  parent_id   = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  path_part   = "syntactical-analysis"
}

resource "aws_api_gateway_method" "syntactical_analysis_post" {
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  resource_id   = aws_api_gateway_resource.syntactical_analysis.id
  http_method   = "POST"
  authorization = "NONE"
}


resource "aws_api_gateway_integration" "syntactical_analysis_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.lingolift_api.id
  resource_id             = aws_api_gateway_resource.syntactical_analysis.id
  http_method             = aws_api_gateway_method.syntactical_analysis_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.syntactical_analysis.lambda_function_invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id

  triggers = {
    redeployment = filesha1("api_gateway.tf")
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