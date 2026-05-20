variable "student_name" {
    description = "Your name in lowercase with hyphens. Must be used to name all resources in this project. For example, if your name is John Doe, you would use 'john-doe'."

    validation {
      condition = can(regex("^[a-z0-9-]+$", var.student_name))
        error_message = "The student_name variable must only contain lowercase letters, numbers, and hyphens, with no spaces or other special characters."
    }

    default = "student-alex-huper"
}

variable "project_name" {
    description = "Project name - combined with student_name to form resource names"
    default = "ems"
}

variable "aws_region" {
    description = "AWS region to deploy resources in"
    type = string
    default = "us-east-1"
}

variable "cohort" {
    description = "Cohort identifier tagged on every resource"
    type = string
    default = "fullstack-aws"
}

variable "jwt_secret_key" {
    description = "Secret key used for signing JWT tokens. Must be at least 32 characters long."
    type = string
    default = "supersecretkey"
}