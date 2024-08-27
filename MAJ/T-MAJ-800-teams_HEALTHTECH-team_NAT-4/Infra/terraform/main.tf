terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-west-3"
}

resource "aws_key_pair" "ssh_key" {
  key_name   = "aws"
  public_key = file("~/.ssh/aws.pub")
}

resource "aws_instance" "Healthtech" {
  ami           = "ami-080c979a925ecf23c"
  instance_type = "t2.micro"

  ebs_block_device {
    device_name = "/dev/xvda"
    volume_size = 10
  }

  key_name        = aws_key_pair.ssh_key.key_name
  security_groups = ["webServers"]

  tags = {
    Name = "Healthtech"
  }
}
