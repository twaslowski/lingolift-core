resource "aws_api_gateway_rest_api" "lingolift_api" {
  name        = "lingolift_api"
  description = "The Lingolift API"
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
  uri                     = module.translation-lambda.invoke_arn
}
