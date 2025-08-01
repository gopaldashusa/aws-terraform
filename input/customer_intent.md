Design a secure, scalable, and cost-effective AWS infrastructure for a document processing workflow.
Components to include:
    - VPC with public/private subnets, IGW/NAT, security groups, and NACLs
    - 2 EC2 instances in private subnet for document processing (with IAM roles and S3 access)
    - S3 bucket (encrypted, access-controlled, with lifecycle policies) for storing documents
    - Lambda function to move files from EC2 to S3 and update RDS with metadata
    - RDS database (encrypted, backed up) to store document metadata (ID, timestamp, S3 link)
Requirements:
    - Follow AWS security best practices
    - Encrypt data in transit and at rest
    - Implement proper IAM roles, monitoring, logging, and alerting
    - Ensure modular design for scalability
    - Stay within a $200/month budget
    - Follow FinOps best practices
    - Complete solution within a 2-week timeline
Deliverables:
    - High-level AWS architecture diagram
    - Infrastucture Implementtion Plan
    - Terraform scripts with proper modules, dependencies, variables, and outputs