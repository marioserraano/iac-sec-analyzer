provider "aws" {
  region = "eu-west-1"
}

resource "aws_s3_bucket" "secure_logs" {
  bucket = "company-secure-logs"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs_encryption" {
  bucket = aws_s3_bucket.secure_logs.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}