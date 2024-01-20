terraform {
  backend "s3" {
    bucket = "lingolift-state"
    key    = "state"
    region = "eu-central-1"
  }
}