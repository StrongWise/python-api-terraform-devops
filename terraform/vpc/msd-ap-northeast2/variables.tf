# ex. 10
variable "cidr_numeral" {
  description = "The VPC CIDR numeral (10.x.0.0/16)"
}

variable "cidr_numeral_public" {
  default = {
    "0" = "0"
    "1" = "32"
  }
}

variable "cidr_numeral_private" {
  default = {
    "0" = "80"
    "1" = "112"
  }
}

# ex. ["ap-northeast-2a","ap-northeast-2c"]
variable "availability_zones" {
  type        = list(string)
  description = "A comma-delimited list of availability zones for the VPC."
}

# ex. vpc-msd-apnortheast2
variable "vpc_name" {
  description = "The name of the VPC"
}
