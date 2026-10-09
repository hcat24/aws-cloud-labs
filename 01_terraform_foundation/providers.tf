provider "aws" {
  profile = "cloud-labs"
  region  = "eu-central-1"
  default_tags {
    tags = {
      project     = "01-terraform-foundation"
      Environment = "lab"
      managedby   = "terraform"
    }
  }
}