# Terraform Foundations

## Goal
Prepare and validate a Terraform configuration for future AWS infrastructure.

## Configuration
- AWS authentication profile: cloud-labs
- AWS Region: eu-central-1 (Frankfurt)
- Terraform version requirement: >= 1.5.0, < 2.0.0
- AWS provider version constraint: ~> 6.0
- Default tags identify the project, environment, and management tool.

## Files
- version.tf: Terraform and AWS provider version requirements.
- providers.tf: AWS profile, region, and default tags.
- .terraform.lock.hcl: Selected provider version and package checksums.

## Completed checks
1. terraform fmt
2. terraform init -backend=false
3. terraform validate

Validation completed successfully.

## Current status
Deployed one S3 bucket in eu-central-1 using Terraform:
- All four Block Public Access settings enabled.
- BucketOwnerEnforced ownership with ACLs disabled.
- Default SSE-S3 encryption using AES256.
- force_destroy disabled.

AWS authentication verified using the cloud-labs profile.
Terraform apply completed: 4 added, 0 changed, 0 destroyed.
A subsequent terraform plan reported no changes.
The bucket was confirmed visible in the AWS Console.

Terraform state is stored locally and excluded from Git.
The saved deployment plan is also excluded from Git.

## Next step
Add outputs for the bucket name and ARN.
Practise uploading and retrieving a small lab file.