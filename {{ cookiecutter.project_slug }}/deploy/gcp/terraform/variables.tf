variable "project_name" {
  type        = string
  description = "Logical name used in resource names."
}

variable "environment" {
  type        = string
  default     = "production"
}

variable "gcp_project_id" {
  type        = string
  description = "GCP project ID."
}

variable "gcp_region" {
  type        = string
  description = "Default region (e.g. us-central1)."
  default     = "us-central1"
}
