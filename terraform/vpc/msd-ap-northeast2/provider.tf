# terraform 블록은 설치할 프로바이더(aws, azure, gcp..)와
# 인프라 프로비저닝(서버준비, 설정과정)
# https://developer.hashicorp.com/terraform/tutorials/aws-get-started/aws-create
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket         = "myservice-dev-apnortheast2-tfstate-1770279863"
    key            = "myservice/terraform/vpc/msd_apnortheast2/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    use_lockfile   = true
  }

  required_version = "~> 1.10"
}

# 리전 검색은 AWS Global View에서
# https://us-east-1.console.aws.amazon.com/awsglobalview/home?region=ap-northeast-2#RegionExplorer
provider "aws" {
  profile = "default"
  region  = "ap-northeast-2"
}
