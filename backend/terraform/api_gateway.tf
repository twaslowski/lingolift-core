resource "aws_api_gateway_rest_api" "lingolift_api" {
  name        = "lingolift_api"
  description = "The Lingolift API"

  body = jsonencode({
    openapi = "3.0.1"
    info    = {
      title   = "lingolift_api"
      version = "1.0"
    }
    paths = {}
  })
}

resource "aws_api_gateway_resource" "translation" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id
  parent_id   = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  path_part   = "translation"
}

resource "aws_api_gateway_method" "translation_post" {
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  resource_id   = aws_api_gateway_resource.translation.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "translation_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.lingolift_api.id
  resource_id             = aws_api_gateway_resource.translation.id
  http_method             = aws_api_gateway_method.translation_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.translation.lambda_function_invoke_arn
}

resource "aws_api_gateway_resource" "literal_translation" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id
  parent_id   = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  path_part   = "literal-translation"
}

resource "aws_api_gateway_method" "literal_translation_post" {
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  resource_id   = aws_api_gateway_resource.literal_translation.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "literal_translation_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.lingolift_api.id
  resource_id             = aws_api_gateway_resource.literal_translation.id
  http_method             = aws_api_gateway_method.literal_translation_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.literal_translation.lambda_function_invoke_arn
}


resource "aws_api_gateway_resource" "response_suggestion" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id
  parent_id   = aws_api_gateway_rest_api.lingolift_api.root_resource_id
  path_part   = "response-suggestion"
}

resource "aws_api_gateway_integration" "response_suggestion_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.lingolift_api.id
  resource_id             = aws_api_gateway_resource.response_suggestion.id
  http_method             = aws_api_gateway_method.response_suggestion_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.response_suggestion.lambda_function_invoke_arn
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

resource "aws_api_gateway_method" "response_suggestion_post" {
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  resource_id   = aws_api_gateway_resource.response_suggestion.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_deployment" "deployment" {
  rest_api_id = aws_api_gateway_rest_api.lingolift_api.id

  triggers = {
    redeployment = sha1(jsonencode(aws_api_gateway_rest_api.lingolift_api.body))
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "dev" {
  depends_on = [aws_cloudwatch_log_group.logs]

  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.lingolift_api.id
  stage_name    = "dev"
}

resource "aws_cloudwatch_log_group" "logs" {
  name              = "API-Gateway-Execution-Logs_${aws_api_gateway_rest_api.lingolift_api.id}/dev"
  retention_in_days = 7
}