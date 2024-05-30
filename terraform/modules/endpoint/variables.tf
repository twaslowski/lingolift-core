variable "name" {
  type = string
}

variable "environment" {
  type = string
}

# API Gateway Resources
variable "root_resource_id" {
  type = string
}

variable "api_gateway_id" {
  type = string
}

# Mandatory Lambda Resources
variable "openai_api_key" {
  type = string
}

variable "handler" {
  type = string
  default = ""
  description = "Entrypoint for the Lambda. Not required for dockerized Lambda functions."
}

variable "package_type" {
  type    = string
  default = "Zip"
}

variable "local_existing_package" {
  type    = string
  default = null
}

variable "image_uri" {
  type    = string
  default = null
}

variable "runtime" {
  type    = string
  default = null
}

variable "layers" {
  type    = list(string)
  default = []
}

variable "memory" {
  type    = number
  default = 128
}

variable "timeout" {
  type    = number
  default = 15
}
