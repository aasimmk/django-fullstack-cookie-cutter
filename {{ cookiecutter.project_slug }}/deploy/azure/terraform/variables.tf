variable "project_name" {
  type = string
}

variable "environment" {
  type    = string
  default = "production"
}

variable "azure_location" {
  type    = string
  default = "eastus"
}
