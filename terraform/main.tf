terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      student = var.student_name
      cohort  = var.cohort
    }
  }
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }

}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]
  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "random_id" "suffix" {
  byte_length = 4
}

locals {
  # All resources follow: student-<name>-<project>-<random-hex>
  # Example: student-alex-huper-ems-a1b2c3d4
  name = "${var.student_name}-${var.project_name}-${random_id.suffix.hex}"
}

# S3 bucket for frontend
resource "aws_s3_bucket" "frontend" {
  bucket = "${local.name}-frontend"
}

resource "aws_s3_bucket_public_access_block" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_website_configuration" "frontend" {
  bucket = aws_s3_bucket.frontend.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}

resource "aws_cloudfront_origin_access_control" "oac" {
  name                              = "${local.name}-oac"
  description                       = "OAC for ${local.name} S3 bucket"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "cdn" {
  enabled             = true
  default_root_object = "index.html"
  origin {
    domain_name              = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id                = "s3-frontend"
    origin_access_control_id = aws_cloudfront_origin_access_control.oac.id
  }

  default_cache_behavior {
    target_origin_id       = "s3-frontend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }



  viewer_certificate {
    cloudfront_default_certificate = true
  }
  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Project = var.project_name
    Student = var.student_name
  }
}

# S3 bucket policy to allow CloudFront OAC to read from the bucket
# Uses distribution of the ARN and not the OAC ARN
resource "aws_s3_bucket_policy" "frontend" {
  bucket = aws_s3_bucket.frontend.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = aws_cloudfront_origin_access_control.oac.arn # Allow access from CloudFront OAC to S3 bucket 
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.frontend.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.cdn.arn # Ensure the request is coming from the correct CloudFront distribution
          }
        }
      }
    ]
  })
}

resource "aws_iam_role" "lambda" {
  name = "${var.student_name}-${var.project_name}-lambda-exec"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_vpc_access" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"
}

# Security Groups
# 2 security groups:
# mongo-sg: for MongoDB EC2 instance to allow inbound on port 22 for SSH and port 27017 for MongoDB, but only from the Lambda SG
# lambda-sg: for Lambda function to allow outbound traffic to MongoDB SG on port 27017

resource "aws_security_group" "lambda_sg" {
  name        = "${local.name}-lambda-sg"
  description = "Security group for Lambda function to access MongoDB"
  vpc_id      = data.aws_vpc.default.id

  egress {
    description = "Allow all outbound traffic for Lambda (e.g. to access AWS services or external APIs)"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "mongo_sg" {
  name        = "${local.name}-mongo-sg"
  description = "Security group for MongoDB EC2 instance"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Allow SSH from anywhere (not recommended for production)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = "Allow MongoDB from Lambda SG"
    from_port       = 27017
    to_port         = 27017
    protocol        = "tcp"
    security_groups = [aws_security_group.lambda_sg.id]
  }

  egress {
    description = "Restrict all outbound traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "mongodb" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.micro"
  subnet_id                   = data.aws_subnets.default.ids[0]
  security_groups             = [aws_security_group.mongo_sg.id]
  key_name                    = var.student_name
  associate_public_ip_address = true

  user_data = <<-EOF
                    #!/bin/bash
                    set -e
                    apt-get update -y
                    apt-get install -y gnupg curl
                    curl -fsSL https://pgp.mongodb.com/server-6.0.asc | gpg --dearmor -o /usr/share/keyrings/mongodb-server-6.0.gpg
                    echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-6.0.list
                    apt-get update -y
                    apt-get install -y mongodb-org
                    sed -i "s/^ bindIp: .*/ bindIp: 0.0.0.0/" /etc/mongod.conf
                    systemctl enable mongod
                    systemctl restart mongod
                EOF
  tags = {
    Name    = "${local.name}-mongodb"
    Project = var.project_name
    Student = var.student_name
  }
}

# Lambda function
resource "aws_lambda_function" "api" {
  function_name = "${var.student_name}-${var.project_name}-api"
  role          = aws_iam_role.lambda.arn
  handler       = "app.main.handler"
  runtime       = "python3.11"
  filename      = "lambda.zip"
  timeout       = 30
  memory_size   = 128

  environment {
    variables = {
      MONGO_URI     = "mongodb://${aws_instance.mongodb.private_ip}:27017"
      MONGO_DB_NAME = "ems_db"

      # security settings
      JWT_SECRET_KEY                  = "dev-secret-key-do-not-use-in-production"
      JWT_ALGORITHM                   = "HS256"
      JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
      JWT_SECRET                      = var.jwt_secret_key
    }
  }

  vpc_config {
    subnet_ids         = [data.aws_subnets.default.ids[0]]
    security_group_ids = [aws_security_group.lambda_sg.id]
  }

  tags = {
    Project = var.project_name
    Student = var.student_name
  }
}

resource "aws_apigatewayv2_api" "api" {
  name          = "${var.student_name}-${var.project_name}-api-gateway"
  protocol_type = "HTTP"


    cors_configuration {
      allow_origins = ["https://${aws_cloudfront_distribution.cdn.domain_name}"]
      allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
      allow_headers = ["Content-Type", "Authorization"]
      max_age = 300
    }
  tags = {
    Project = var.project_name
    Student = var.student_name
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.api.invoke_arn
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_route" "proxy" {
  api_id    = aws_apigatewayv2_api.api.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "default" {
  api_id    = aws_apigatewayv2_api.api.id
  name = "$default"
  auto_deploy = true
}

resource "aws_lambda_permission" "apigw" {
    statement_id = "AllowAPIGatewayInvoke"
    action       = "lambda:InvokeFunction"
    function_name = aws_lambda_function.api.function_name
    principal    = "apigateway.amazonaws.com"
    source_arn   = "${aws_apigatewayv2_api.api.execution_arn}/*/*"
}