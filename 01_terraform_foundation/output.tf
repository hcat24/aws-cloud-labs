output "bucket_name" {
  value       = aws_s3_bucket.storage.id
  description = "The name of the S3 bucket"
}
output "bucket_arn" {
  value       = aws_s3_bucket.storage.arn
  description = "The arn of the bucket"
}