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

# ex. ["ap-northeast-2a","ap-northeast-2c"]
variable "availability_zones" {
  type        = list(string)
  description = "A comma-delimited list of availability zones for the VPC."
}

# ex. msd-apnortheast2-vpc
variable "vpc_name" {
  description = "The name of the VPC"
}
