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
No AWS resources have been deployed.
Backend initialization was skipped for this validation milestone.
AWS authentication and deployment permissions have not been tested by these checks.

## Next step
Define a private S3 bucket, validate the configuration, and review
permissions and estimated costs before deployment.