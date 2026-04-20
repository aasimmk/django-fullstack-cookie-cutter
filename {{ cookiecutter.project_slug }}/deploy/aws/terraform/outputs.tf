output "ecr_repository_url" {
  description = "Push Docker images here."
  value       = aws_ecr_repository.app.repository_url
}

output "media_bucket" {
  description = "S3 bucket for user uploads / static media."
  value       = aws_s3_bucket.media.bucket
}
