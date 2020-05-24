# Terraform Setup of our VPS

# Set up Static IP
resource "aws_lightsail_static_ip" "static_ip_ire" {
  name = "StaticIP-Ireland-1"
}

# Set up domain name
resource "aws_lightsail_domain" "groganburners_ie" {
  domain_name = "groganburners.ie"
}

# Set up domain name
resource "aws_lightsail_domain" "groganburners_com" {
  domain_name = "groganburners.com"
}

# Upload our SSH Public Key
resource "aws_lightsail_key_pair" "personal_key_pair" {
  name       = "id_personal"
  public_key = "file('~/.ssh/id_personal.pub')"
}

# Create a new Lightsail Instance
resource "aws_lightsail_instance" "gbs_vps" {
  name              = "Ubuntu18.04-1GB-Ireland1"
  availability_zone = "eu-west-1a"
  blueprint_id      = "ubuntu_18_04"
  bundle_id         = "micro_2_0"
  key_pair_name     = "id_personal"
}

# Attach Static IP to our New Instance
resource "aws_lightsail_static_ip_attachment" "test" {
  static_ip_name = "aws_lightsail_static_ip.static_ip_ire.id"
  instance_name  = "aws_lightsail_instance.gbs_vps.id"
}
