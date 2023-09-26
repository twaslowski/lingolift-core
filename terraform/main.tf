resource "aws_lightsail_instance" "my_lightsail_instance" {
  name               = "lingolift"
  availability_zone  = "eu-central-1a"
  blueprint_id       = "amazon_linux_2"
  bundle_id          = "nano_2_0"

  key_pair_name      = aws_lightsail_key_pair.my_key_pair.name
  user_data = file("${path.module}/userdata.sh")
}

resource "aws_lightsail_key_pair" "my_key_pair" {
  name = "lingolift-keypair"
}
