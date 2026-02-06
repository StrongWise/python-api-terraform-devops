output "aws_security_group_bastion_id" {
  value = aws_security_group.bastion.id
}

output "public_subnets" {
  value = aws_subnet.public.*.id
}

output "private_subnets" {
  value = aws_subnet.private.*.id
}

output "vpc_id" {
  value = aws_vpc.default.id
}

output "security_group_ids" {
  value = [aws_security_group.bastion.id]
}

output "alb_security_group_id" {
  value = aws_security_group.alb_sg.id
}
