variable "openai_api_key" {
  type = string
}

variable "name" {
  type = string
}

variable "memory_size" {
  type = number
  default = 512
}

variable "timeout" {
  type = number
  default = 15
}