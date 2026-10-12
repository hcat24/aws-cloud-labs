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

## Terraform-managed file deployment
- Added outputs for the bucket name and ARN.
- Practised uploading and downloading objects with the AWS CLI.
- Used fileset and for_each to manage files from the uploads folder.
- Used source_hash to detect changes to local file contents.
- Deployed uploads/note.txt and tested a content update.

Adding files proposes new S3 objects.
Changing files proposes updates.
Removing files proposes deletion of their managed S3 objects.
Uploads occur when terraform apply runs.

## Planned extension
Build a Python folder watcher that uploads arriving files
under incoming/, separate from Terraform-managed uploads/.