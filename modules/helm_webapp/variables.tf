variable "helm_release_name" {
  type        = string
  description = "Name of the Helm release"
}

variable "namespace" {
  type        = string
  description = "Kubernetes namespace"
}

variable "image_repository" {
  type        = string
  description = "Docker image repository URL"
}

variable "image_tag" {
  type        = string
  description = "Docker image tag"
  default     = "latest"
}

variable "hello_world_message" {
  type        = string
  description = "Configurable hello world message for the web application"
  default     = "Hello from Terraform!"
}