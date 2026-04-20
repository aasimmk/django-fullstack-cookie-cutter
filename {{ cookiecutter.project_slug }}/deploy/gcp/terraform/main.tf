terraform {
  required_version = ">= 1.5.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}

resource "google_storage_bucket" "media" {
  name                        = "${var.project_name}-${var.environment}-media"
  location                    = var.gcp_region
  uniform_bucket_level_access = true
}

resource "google_artifact_registry_repository" "app" {
  location      = var.gcp_region
  repository_id = "${var.project_name}-${var.environment}-app"
  description   = "Docker images for {{ cookiecutter.project_slug }}"
  format        = "DOCKER"
}
