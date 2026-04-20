output "artifact_registry_repository" {
  value       = google_artifact_registry_repository.app.name
  description = "Repository id for docker push."
}

output "media_bucket" {
  value       = google_storage_bucket.media.name
  description = "GCS bucket for uploads."
}
