# vulnerable.tf

# 1. Hardcoded Credentials (CRITICAL)
provider "aws" {
  region     = "us-east-1"
  access_key = "AKIA1234567890EXAMPLE"
  secret_key = "SuperSecretPassword123!"
}

# 2. Publicly Exposed Resource (HIGH)
resource "aws_security_group" "web_sg" {
  name        = "web_server_sg"
  description = "Allow all inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # SSH exposed to the whole internet!
  }
}

# 3. Excessive IAM Permissions (HIGH)
resource "aws_iam_policy" "admin_policy" {
  name        = "super_admin_policy"
  description = "Policy with wildcard permissions"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action   = "*"
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}

# 4. Lack of Encryption at Rest (MEDIUM)
resource "aws_s3_bucket" "company_data" {
  bucket = "company-sensitive-data-2024"
  # Missing the aws_s3_bucket_server_side_encryption_configuration block
}