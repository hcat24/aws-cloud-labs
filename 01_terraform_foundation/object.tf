resource "aws_s3_object" "file" {
  for_each    = fileset("${path.module}/uploads", "**")
  bucket      = aws_s3_bucket.storage.id
  key         = "uploads/${each.value}"
  source      = "${path.module}/uploads/${each.value}"
  source_hash = filemd5("${path.module}/uploads/${each.value}")

}