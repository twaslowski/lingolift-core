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

# todo it turns out the issue is the AWS_PROXY integration type
# when choosing a non-proxy resource everything works exactly as expected
resource "aws_api_gateway_integration" "translation_lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.lingolift_api.id
  resource_id             = aws_api_gateway_resource.translation.id
  http_method             = aws_api_gateway_method.translation_post.http_method
  integration_http_method = "POST"
  type                    = "AWS"
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
  resource_id             = aws_api_gateway_resource.translation.id
  http_method             = aws_api_gateway_method.translation_post.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = module.literal_translation.lambda_function_invoke_arn
}