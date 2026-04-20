variable "project_name" {
  type        = string
  description = "Logical project name used for tagging."
}

variable "environment" {
  type        = string
  description = "Deployment environment (e.g. staging, production)."
  default     = "production"
}

variable "aws_region" {
  type        = string
  description = "AWS region for all resources."
  default     = "us-east-1"
}
