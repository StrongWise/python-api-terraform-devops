data "terraform_remote_state" "vpc" {
  backend = "s3"

  config = {
    bucket       = var.remote_state_bucket
    region       = var.remote_state_region
    key          = var.remote_state_key_map["vpc"]
  }
}
