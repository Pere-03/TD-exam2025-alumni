terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.5.0"
    }
  }
}

provider "google" {
  credentials = file("../../exam-458209-b7fa83e6b3e1.json")

  project = var.gcp-project
  region  = var.gcp-region
  zone    = var.gcp-zone
}
