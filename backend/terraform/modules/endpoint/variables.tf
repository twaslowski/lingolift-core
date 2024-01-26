variable "name" {
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
  type    = string
}

variable "package_type" {
    type    = string
    default = "Zip"
}

variable "local_existing_package" {
    type    = string
    default = ""
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
