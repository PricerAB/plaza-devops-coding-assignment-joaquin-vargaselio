terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }

  required_version = ">= 1.3.0"

  backend "gcs" {
    bucket = "code-assignment-terraform-state"
    prefix = "plaza-devops/terraform/state"
  }
}
