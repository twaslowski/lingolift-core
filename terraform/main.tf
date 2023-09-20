resource "aws_lightsail_instance" "my_lightsail_instance" {
  name               = "lingolift-static"
  availability_zone  = "eu-central-1a" # Match the region in the provider configuration
  blueprint_id       = "amazon_linux_2" # This is for Amazon Linux 2 OS only
  bundle_id          = "nano_2_0" # This is for the $3.50/month plan

  # Optional: To add your SSH key to the instance
  key_pair_name      = aws_lightsail_key_pair.my_key_pair.name
  user_data = file("${path.module}/userdata.sh")
}

resource "aws_lightsail_key_pair" "my_key_pair" {
  name = "lingolift-keypair"
}
