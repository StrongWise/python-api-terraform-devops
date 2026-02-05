variable "cidr_numeral" {
  description = "The VPC CIDR numeral (10.x.0.0/16)"
}

variable "cidr_numeral_public" {
  default = {
    "0" = "0"
    "1" = "32"
  }
}

variable "availability_zones" {
  type        = list(string)
  description = "A comma-delimited list of availability zones for the VPC."
}

variable "vpc_name" {
  description = "The name of the VPC"
}
