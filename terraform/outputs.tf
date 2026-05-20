output "cloudfront_url" {
  description = "Frontend URL - open this in the browser"
  value = "https://${aws_cloudfront_distribution.cdn.domain_name}"
}

output "api_url" {
  description = "API Gateway URL - set as VITE_API_URL in frontend .env file"
  value = aws_apigatewayv2_api.api.api_endpoint
}

output "s3_bucket_name" {
  description = "S3 bucket name for storing frontend assets"
  value = aws_s3_bucket.frontend.bucket
}

output "lambda_function_name" {
  description = "Name of the Lambda function for backend logic"
  value = aws_lambda_function.api.function_name
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID for cache invalidation"
  value = aws_cloudfront_distribution.cdn.id
}

output "mongo_public_ip" {
  description = "Public IP address of the MongoDB EC2 instance for direct access (not recommended for production)"
  value = aws_instance.mongodb.public_ip
}

output "mongo_private_ip" {
  description = "Private IP address of the MongoDB EC2 instance for secure access from Lambda"
  value = aws_instance.mongodb.private_ip
}