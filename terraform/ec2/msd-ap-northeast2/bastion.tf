resource "aws_instance" "bastion" {
  ami                    = "ami-02eb6e33da0d2c404"
  key_name               = "msd-dev"
  instance_type          = "t4g.nano"
  vpc_security_group_ids = [data.terraform_remote_state.vpc.outputs.aws_security_group_bastion_id]
  private_ip             = "10.10.10.10"
  subnet_id              = data.terraform_remote_state.vpc.outputs.public_subnets[0]

  tags = {
    Name = "bastion"
  }
}
