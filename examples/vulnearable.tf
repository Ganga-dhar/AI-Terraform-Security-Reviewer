provider "aws" {
  region = "ap-south-1"
}

resource "aws_s3_bucket" "application_data" {
  bucket = "my-company-application-data"

  acl = "public-read"
}

resource "aws_security_group" "application" {
  name = "application-sg"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_iam_policy" "application" {
  name = "application-policy"

  policy = jsonencode({
    Version = "2012-10-17"

    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}



//We intentionally created vulnerabilities.: vulnerabilities.tf

//The AI should eventually detect:

//S3 public access
//S3 encryption missing
//SSH exposed to internet
//Excessive IAM permissions
//Resource "*" permissions