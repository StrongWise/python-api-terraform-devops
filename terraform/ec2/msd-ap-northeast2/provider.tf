terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket       = "myservice-dev-apnortheast2-tfstate-1770279863"
    key          = "myservice/terraform/ec2/msd_apnortheast2/terraform.tfstate"
    region       = "ap-northeast-2"
    encrypt      = true
    use_lockfile = true
  }

  required_version = "~> 1.10"
}

provider "aws" {
  profile = "default"
  region  = "ap-northeast-2"
}
