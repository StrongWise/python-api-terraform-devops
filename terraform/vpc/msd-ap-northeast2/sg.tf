# Security Group to the bastion server
# 22포트만 외부 허용, 나머지 내부망에서만 접근
resource "aws_security_group" "bastion" {
  name        = "bastion-${var.vpc_name}"
  description = "Allows SSH access to the bastion server"

  vpc_id = aws_vpc.default.id

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = ["10.10.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "bastion-${var.vpc_name}"
  }
}

# Security Group to the bastion server
resource "aws_security_group" "alb_sg" {
  name        = "alb-${var.vpc_name}"
  description = "Allows ALB access"

  vpc_id = aws_vpc.default.id

  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"

    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = ["10.10.0.0/16"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "alb-${var.vpc_name}"
  }
}
