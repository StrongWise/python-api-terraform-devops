# precondition

1. You must create private key with key name as "msd-dev" 
2. You must create dynamo db table as "myservice_deployment_versions"
3. You must create s3 bucket with "myservice-dev-apnortheast2-tfstate"

# How to run terraform

1. terraform init
2. terraform plan -out "output"
3. terraform apply "output"
