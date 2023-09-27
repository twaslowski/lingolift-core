resource "aws_lightsail_instance" "my_lightsail_instance" {
  name              = "lingolift"
  availability_zone = "eu-central-1a"
  blueprint_id      = "amazon_linux_2"
  bundle_id         = "micro_2_0"

  key_pair_name = "lightsail-key.pem"
  user_data     = file("${path.module}/userdata.sh")
}


resource "aws_lightsail_static_ip" "static_ip" {
  name = "lingolift_static"
}

resource "aws_lightsail_static_ip_attachment" "static_ip_attachment" {
  static_ip_name = aws_lightsail_static_ip.static_ip.name
  instance_name  = aws_lightsail_instance.my_lightsail_instance.name
}