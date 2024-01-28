resource "aws_api_gateway_api_key" "key" {
  name = "key-${var.environment}"
}

resource "aws_api_gateway_usage_plan_key" "usage_key" {
  key_id        = aws_api_gateway_api_key.key.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage_plan.id
}

resource "aws_api_gateway_usage_plan" "usage_plan" {
  name        = "${var.environment}-usage-plan}"
  description = "usage plan for lingolift api gateway"

  api_stages {
    api_id = aws_api_gateway_rest_api.lingolift_api.id
    stage  = aws_api_gateway_stage.stage.stage_name
  }

  quota_settings {
    limit  = 1000
    offset = 0
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 20
    rate_limit  = 100
  }
}