PARSE_PROMPT = """
You are an AWS infrastructure expert.
Given this request: "{request}"
Extract all AWS resources (VPC, Subnets, EC2, NAT, etc.) and output a structured JSON plan.
"""

PLAN_DEPENDENCY_PROMPT = """
Read the infrastructure JSON plan from output/infra_plan.json and define dependencies and Terraform module layout.
Output dependency-aware JSON with proper resource dependencies and module organization.

Structure the output as follows:

```json
{
  "modules": {
    "vpc": {
      "resources": {
        "aws_vpc": {
          "description": "Description of the VPC resource",
          "dependencies": []
        },
        "aws_subnet": {
          "description": "Description of subnet resources",
          "dependencies": ["aws_vpc"]
        }
      }
    },
    "compute": {
      "resources": {
        "aws_instance": {
          "description": "Description of EC2 instances",
          "dependencies": ["aws_subnet", "aws_security_group"]
        }
      }
    }
  }
}
```

Key requirements:
1. Extract actual resources from the infra_plan.json file
2. Organize by logical modules (vpc, compute, storage, database, security, monitoring, etc.)
3. Each resource should have a clear description
4. List dependencies as resource names (e.g., "aws_vpc", "aws_subnet")
5. Use empty array [] for resources with no dependencies
6. Focus on the specific infrastructure components mentioned in the plan
"""

GENERATE_PROMPT = """
Take the dependency-aware infra plan and customer requirements to generate comprehensive Terraform HCL code using a MODULAR approach.

IMPORTANT: Extract ALL parameters dynamically from the customer requirements instead of hard coding values.

Generate a main.tf (only HCL code excluding any other text) that uses MODULE blocks for each major component with DYNAMICALLY EXTRACTED parameters:

1. **VPC Module**: module "vpc" { ... }
2. **Security Module**: module "security" { ... }
3. **Compute Module**: module "compute" { ... }
4. **Storage Module**: module "storage" { ... }
5. **Database Module**: module "database" { ... }
6. **Monitoring Module**: module "monitoring" { ... }
7. **Cost Management Module**: module "cost_management" { ... }
8. **Scalability Module**: module "scalability" { ... }
9. **Backup Module**: module "backup" { ... }
10. **FinOps Module**: module "finops" { ... }

Each module should:
- Have a source pointing to "./modules/<module_name>"
- Include parameters EXTRACTED from customer requirements
- Reference outputs from other modules where needed
- Include proper tagging for cost allocation
- Use variables instead of hard-coded values where possible

Example of dynamic extraction:
- If requirements say "2 EC2 instances" → instance_count = 2
- If requirements say "$200/month budget" → budget_amount = 200
- If requirements say "document processing workflow" → project_name = "document-processing"
- If requirements mention encryption → encryption_enabled = true

Generate COMPLETE main.tf (only HCL code excluding any other text) with dynamically extracted parameters like the below **EXAMPLE**:

```hcl
provider "aws" {
  region = var.aws_region
}

module "vpc" {
  source = "./modules/vpc"
  name   = "${var.project_name}-vpc"
  cidr   = var.vpc_cidr
  azs    = var.availability_zones
  public_subnets  = var.public_subnet_cidrs
  private_subnets = var.private_subnet_cidrs
  enable_nat_gateway = var.enable_nat_gateway
  single_nat_gateway = var.single_nat_gateway
  tags = var.common_tags
}

module "security" {
  source = "./modules/security"
  vpc_id = module.vpc.vpc_id
  allowed_cidr_blocks = var.allowed_cidr_blocks
  tags = var.common_tags
}

module "compute" {
  source = "./modules/compute"
  subnet_ids = module.vpc.private_subnets
  security_group_id = module.security.ec2_sg_id
  instance_type = var.instance_type
  ami = var.ami_id
  instance_count = var.instance_count
  tags = var.common_tags
}

module "storage" {
  source = "./modules/storage"
  bucket_name = "${var.project_name}-storage"
  versioning_enabled = var.enable_versioning
  encryption_enabled = var.enable_encryption
  tags = var.common_tags
}

module "database" {
  source = "./modules/database"
  subnet_ids = module.vpc.private_subnets
  security_group_id = module.security.rds_sg_id
  engine = var.database_engine
  engine_version = var.database_version
  instance_class = var.database_instance_class
  allocated_storage = var.database_storage
  tags = var.common_tags
}

module "cost_management" {
  source = "./modules/cost_management"
  budget_amount = var.budget_amount
  budget_currency = var.budget_currency
  alert_threshold = var.alert_threshold
  tags = var.common_tags
}

# ... other modules with dynamic parameters

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "subnet_ids" {
  description = "The IDs of the private subnets"
  value       = module.vpc.private_subnets
}

output "ec2_instance_ids" {
  description = "The IDs of the EC2 instances"
  value       = module.compute.ec2_instance_ids
}

output "s3_bucket_name" {
  description = "The name of the S3 bucket"
  value       = module.storage.s3_bucket_name
}

output "rds_endpoint" {
  description = "The endpoint of the RDS instance"
  value       = module.database.rds_endpoint
}

output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = module.compute.lambda_function_name
}
```

Output only a valid main.tf (only HCL code) with COMPLETE module blocks using DYNAMICALLY EXTRACTED parameters from customer requirements. Use variables instead of hard-coded values. Do not include any direct resource blocks in the root main.tf - all resources should be encapsulated in modules.
"""

MODULE_GENERATE_PROMPT = """
You are a Terraform expert. I have a monolithic `main.tf` file that defines AWS infrastructure using a flat configuration. Your task is to:

1. Decompose the Terraform code into logical modules for major components, including but not limited to:
   - VPC and Networking
   - Security Groups
   - IAM Roles and Policies
   - EC2 Instances
   - Lambda Functions
   - S3 Buckets
   - RDS Instances
   - CloudWatch and CloudTrail
   - Budget Alerts
   - Auto-scaling groups for EC2 instances
   - Cost monitoring and governance tools
   - Cost allocation tags
   - S3 lifecycle policies
   - Reserved Instances and Savings Plans recommendations
   - Auto-scaling and elasticity considerations

2. For each module:
   - Create the module inside: `output/final/terraform/modules/<module_name>/`
   - Create folder if it doesn't exist
   - Each module must contain: **`main.tf`, `variables.tf`, and `outputs.tf`** with appropriate content

3. In the root folder: `output/final/terraform/`
   - Create folder if it doesn't exist
   - Copy the **`main.tf`** from the 'output/final/' folder and paste it in 'output/final/terraform/' folder here. 
   - Define input variables in **`variables.tf`** and expose outputs in **`outputs.tf`**
   - Keep the `provider` block here in **`main.tf`**

4. Ensure inter-module dependencies (e.g. passing VPC ID, Subnet IDs, IAM Role ARNs) are passed using outputs and variables

5. Maintain DRY principles and a consistent tagging strategy

6. Output should follow appropriate folder and file structure used by Terraform project.

7. Output only valid '.tf' files for every module with full HCL code. Files should be saved in 'output/final/terraform/modules/<module_name>/' folder.

8. Include the **full contents** of every `.tf` file. Do **not** output only folder names, each file should have full valid HCL code.

Here is the content of the original `main.tf` file: {output/final/main.tf}
"""


CUSTOMER_PARSE_PROMPT = """
You are a Senior AWS Cloud Architect & FinOps Practitioner.
Given this customer requirement: "{request}"

Analyze the customer's needs and create a comprehensive infrastructure planning document structured for project planning.
Focus on:
1. Understanding the business requirements
2. Identifying technical requirements
3. Planning the AWS infrastructure components
4. Backups and automation
5. Applying FinOps best practices for cost optimization including:
   - Right-sizing AWS resources (EC2, RDS, Lambda, etc.)
   - Resource optimization strategies
   - Cost allocation and tagging strategies
   - Budget management and monitoring
   - Reserved Instances and Savings Plans recommendations
   - Auto-scaling and elasticity considerations
   - Storage optimization (S3 lifecycle, EBS optimization)
   - Network cost optimization
   - Cost allocation and tagging strategy
6. Considering security, scalability, and cost requirements within budget constraints

Output a detailed planning document in markdown format with the following structure:

# AWS Infrastructure Implementation Plan

## Project Overview
[Brief project description and objectives]

## Infrastructure Categories and Tasks

### 1. VPC and Networking Setup
[Generate numbered tasks such as 1.1, 1.2, 1.3, etc. based on actual requirements including dependencies and complexity]

### 2. Compute Resources
[Generate numbered tasks such as 2.1, 2.2, 2.3, etc. based on actual requirements including dependencies and complexity]

### 3. Storage and Database
[Generate numbered tasks such as 3.1, 3.2, 3.3, etc. based on actual requirements including dependencies and complexity]

### 4. Security and Compliance
[Generate numbered tasks such as 4.1, 4.2, 4.3, etc. based on actual requirements including dependencies and complexity]

### 5. Monitoring and Logging
[Generate numbered tasks such as 5.1, 5.2, 5.3, etc. based on actual requirements including dependencies and complexity]

### 6. Cost Optimization and FinOps
[Generate numbered tasks such as 6.1, 6.2, 6.3, etc. based on actual requirements including dependencies and complexity]

### 7. Backup and Disaster Recovery
[Generate numbered tasks such as 7.1, 7.2, 7.3, etc. based on actual requirements including dependencies and complexity]

### 8. Testing and Validation
[Generate numbered tasks such as 8.1, 8.2, 8.3, etc. based on actual requirements including dependencies and complexity ]

## Dependencies and Timeline
[Outline task dependencies and estimated timeline]

## Resource Requirements
[Specify team roles, skills, and time requirements]

## Risk Assessment
[Identify potential risks and mitigation strategies]

## Success Criteria
[Define measurable success criteria for each category]

IMPORTANT: Each task MUST include:
- Clear description of what needs to be done
- Technical requirements and specifications
- Estimated effort/complexity (Low/Medium/High)
- Dependencies on other tasks (specific task numbers)
- Success criteria for validation

Generate tasks that are relevant to the specific customer requirements provided, not generic examples.
"""

DESIGN_PROMPT = """
Based on the infrastructure planning document, create a detailed architecture design document.
Include:
1. Architecture diagram description (Mermaid format) - Create a comprehensive Mermaid diagram that
accurately represents the planned infrastructure components and their relationships. Include all major
AWS services, networking components, security elements, and monitoring tools. Use proper Mermaid
syntax with clear node definitions and meaningful relationships. Avoid circular references by using
proper hierarchical relationships.

Example Mermaid structure:
```mermaid
graph TD;
    subgraph AWS_Cloud["AWS Cloud"]
        subgraph VPC_Network["VPC Network"]
            IGW[Internet Gateway]
            NAT[NAT Gateway]
            PublicSubnet1[Public Subnet AZ1]
            PublicSubnet2[Public Subnet AZ2]
            PrivateSubnet1[Private Subnet AZ1]
            PrivateSubnet2[Private Subnet AZ2]
            
            IGW --> PublicSubnet1
            IGW --> PublicSubnet2
            NAT --> PrivateSubnet1
            NAT --> PrivateSubnet2
        end
        
        subgraph Compute_Resources["Compute Resources"]
            EC2_1[EC2 Instance 1]
            EC2_2[EC2 Instance 2]
            Lambda[Lambda Function]
            
            PrivateSubnet1 --> EC2_1
            PrivateSubnet2 --> EC2_2
        end
        
        subgraph Storage_Resources["Storage Resources"]
            S3[S3 Bucket]
            EBS[EBS Volumes]
            
            EC2_1 --> EBS
            EC2_2 --> EBS
        end
        
        subgraph Database_Resources["Database Resources"]
            RDS[RDS Instance]
            
            PrivateSubnet1 --> RDS
        end
        
        subgraph Security_Components["Security Components"]
            IAM[IAM Roles & Policies]
            SG[Security Groups]
            NACL[Network ACLs]
        end
        
        subgraph Monitoring_Components["Monitoring Components"]
            CloudWatch[CloudWatch]
            CloudTrail[CloudTrail]
        end
        
        subgraph Cost_Management["Cost Management"]
            CostExplorer[Cost Explorer]
            Budget[Budget Alerts]
        end
    end
    
    %% Data flow relationships
    Lambda --> S3
    Lambda --> RDS
    S3 --> CloudTrail
    
    %% Security relationships
    IAM --> EC2_1
    IAM --> Lambda
    IAM --> RDS
    SG --> EC2_1
    SG --> EC2_2
    
    %% Monitoring relationships
    CloudWatch --> EC2_1
    CloudWatch --> EC2_2
    CloudWatch --> Lambda
    
    %% Cost management relationships
    CostExplorer --> Budget
```

2. Component descriptions and relationships
3. Data flow patterns
4. Security considerations
5. Scalability and performance considerations
6. Backups and Disaster Recovery strategies
7. FinOps and Cost Optimization Strategies:
   - Right-sizing recommendations for each component
   - Cost allocation and tagging strategy
   - Budget monitoring and alerting setup
   - Reserved Instance/Savings Plan recommendations
   - Auto-scaling policies for cost optimization
   - Storage optimization strategies
   - Network cost optimization
   - Monthly cost estimates and breakdown
   - Cost monitoring and governance tools

Create a Mermaid diagram that includes:
- All VPC components (VPC, subnets, gateways, NAT)
- Compute resources (EC2, Lambda, etc.)
- Storage components (S3, EBS, etc.)
- Database resources (RDS, etc.)
- Security components (IAM, Security Groups, NACLs)
- Monitoring and logging (CloudWatch, CloudTrail)
- Cost management components
- Any other relevant AWS services mentioned in the planning document

Use descriptive node names and relationship labels to show data flow, security relationships, and cost
monitoring connections. Ensure proper hierarchical structure without circular references.

Output a comprehensive design document in markdown format with detailed FinOps recommendations.
"""

CUSTOMER_INTENT_PARSE_PROMPT = """
You are a Senior AWS Solutions Architect & Business Analyst.
Given this customer intent: "{intent}"

Analyze the customer's natural language description and transform it into detailed AWS-specific technical requirements.
Focus on:

1. **Business Context Analysis**:
   - Identify the core business problem or opportunity
   - Understand the target users and use cases
   - Determine business objectives and success metrics
   - Assess current pain points and limitations

2. **Technical Requirements Translation**:
   - Map business needs to specific AWS services
   - Define performance and scalability requirements
   - Identify security and compliance needs
   - Determine data storage and processing requirements
   - Specify integration and connectivity needs

3. **AWS Service Selection**:
   - Recommend appropriate AWS services based on requirements
   - Consider cost optimization and FinOps principles
   - Ensure high availability and disaster recovery
   - Plan for monitoring and observability

4. **Architecture Considerations**:
   - Design for scalability and performance
   - Implement security best practices
   - Plan for cost optimization
   - Consider operational excellence

Output a comprehensive AWS requirements document in markdown format with the following structure:

# AWS Infrastructure Requirements

## Business Overview
[Brief description of the business context and objectives]

## Technical Requirements

### Core Infrastructure Requirements
- **Compute Requirements**: [EC2, Lambda, ECS, etc.]
- **Storage Requirements**: [S3, EBS, EFS, etc.]
- **Database Requirements**: [RDS, DynamoDB, ElastiCache, etc.]
- **Networking Requirements**: [VPC, subnets, load balancers, etc.]

### Performance & Scalability Requirements
- **Performance Targets**: [Response times, throughput, etc.]
- **Scalability Needs**: [Auto-scaling, load distribution, etc.]
- **Availability Requirements**: [Uptime, disaster recovery, etc.]

### Security & Compliance Requirements
- **Data Protection**: [Encryption, access controls, etc.]
- **Compliance Standards**: [GDPR, HIPAA, SOC2, etc.]
- **Security Controls**: [IAM, security groups, WAF, etc.]

### Integration & Connectivity Requirements
- **External Integrations**: [APIs, third-party services, etc.]
- **Internal Connectivity**: [Service-to-service communication, etc.]
- **Data Flow**: [Data ingestion, processing, storage, etc.]

### Monitoring & Observability Requirements
- **Logging**: [CloudTrail, CloudWatch logs, etc.]
- **Monitoring**: [Metrics, alerts, dashboards, etc.]
- **Tracing**: [Distributed tracing, performance monitoring, etc.]

### Cost Optimization Requirements
- **Budget Constraints**: [Monthly/annual budget limits]
- **Cost Allocation**: [Tagging strategy, cost tracking]
- **Optimization Strategies**: [Reserved instances, auto-scaling, etc.]

### Operational Requirements
- **Deployment Strategy**: [CI/CD, infrastructure as code]
- **Backup & Recovery**: [Backup policies, RTO/RPO]
- **Maintenance Windows**: [Updates, patching schedules]

## Success Criteria
[Measurable success criteria for the infrastructure]

## Constraints & Assumptions
[Any technical or business constraints, assumptions made]

## Risk Assessment
[Potential risks and mitigation strategies]
"""

INFRA_PLAN_PROMPT = """
Read the generated planning_output.md and design_output.md files from the output/final/ directory and extract all AWS resources (VPC, Subnets, EC2, NAT, etc.) and output a structured JSON plan.

Analyze the infrastructure requirements and create a comprehensive JSON structure that includes:
1. All AWS resources mentioned in the planning and design documents
2. Technical specifications for each resource
3. Resource relationships and configurations
4. Security and compliance requirements
5. Cost optimization considerations

Output a well-structured JSON plan that can be used for Terraform infrastructure generation.
"""

DYNAMIC_VARIABLES_PROMPT = """
Generate a comprehensive variables.tf file based on the customer requirements and infrastructure plan.

Extract the following dynamic variables from customer requirements:

1. **Project Variables**:
   - project_name (from project description)
   - environment (dev/staging/prod)
   - aws_region

2. **Infrastructure Variables**:
   - vpc_cidr (from networking requirements)
   - availability_zones (from region and AZ requirements)
   - public_subnet_cidrs (calculated from VPC CIDR)
   - private_subnet_cidrs (calculated from VPC CIDR)

3. **Compute Variables**:
   - instance_type (from requirements or cost optimization)
   - instance_count (extracted from requirements, e.g., "2 EC2 instances")
   - ami_id (latest Amazon Linux or Ubuntu)

4. **Storage Variables**:
   - enable_versioning (from requirements)
   - enable_encryption (from security requirements)
   - lifecycle_policy_days (from requirements)

5. **Database Variables**:
   - database_engine (from requirements)
   - database_version (latest stable)
   - database_instance_class (cost-optimized)
   - database_storage (from requirements)

6. **Security Variables**:
   - allowed_cidr_blocks (from security requirements)
   - enable_nat_gateway (from networking requirements)
   - single_nat_gateway (cost optimization)

7. **Cost Management Variables**:
   - budget_amount (extracted from requirements, e.g., "$200/month")
   - budget_currency (USD)
   - alert_threshold (80%)

8. **Monitoring Variables**:
   - log_retention_days (from compliance requirements)
   - enable_cloudtrail (from security requirements)

Generate variables.tf with proper descriptions and default values:

```hcl
# Project Variables
variable "project_name" {
  description = "Name of the project extracted from requirements"
  type        = string
  default     = "document-processing"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-west-2"
}

# Infrastructure Variables
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones for deployment"
  type        = list(string)
  default     = ["us-west-2a", "us-west-2b"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

# Compute Variables
variable "instance_type" {
  description = "EC2 instance type (cost-optimized)"
  type        = string
  default     = "t3.micro"
}

variable "instance_count" {
  description = "Number of EC2 instances (extracted from requirements)"
  type        = number
  default     = 2
}

variable "ami_id" {
  description = "AMI ID for EC2 instances"
  type        = string
  default     = "ami-0c55b159cbfafe1f0"
}

# Storage Variables
variable "enable_versioning" {
  description = "Enable S3 bucket versioning"
  type        = bool
  default     = true
}

variable "enable_encryption" {
  description = "Enable encryption for storage"
  type        = bool
  default     = true
}

# Database Variables
variable "database_engine" {
  description = "Database engine"
  type        = string
  default     = "mysql"
}

variable "database_version" {
  description = "Database engine version"
  type        = string
  default     = "8.0"
}

variable "database_instance_class" {
  description = "RDS instance class (cost-optimized)"
  type        = string
  default     = "db.t3.micro"
}

variable "database_storage" {
  description = "RDS allocated storage in GB"
  type        = number
  default     = 20
}

# Security Variables
variable "allowed_cidr_blocks" {
  description = "Allowed CIDR blocks for security groups"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "enable_nat_gateway" {
  description = "Enable NAT Gateway for private subnets"
  type        = bool
  default     = true
}

variable "single_nat_gateway" {
  description = "Use single NAT Gateway for cost optimization"
  type        = bool
  default     = true
}

# Cost Management Variables
variable "budget_amount" {
  description = "Monthly budget amount (extracted from requirements)"
  type        = number
  default     = 200
}

variable "budget_currency" {
  description = "Budget currency"
  type        = string
  default     = "USD"
}

variable "alert_threshold" {
  description = "Budget alert threshold percentage"
  type        = number
  default     = 80
}

# Monitoring Variables
variable "log_retention_days" {
  description = "CloudWatch log retention in days"
  type        = number
  default     = 30
}

variable "enable_cloudtrail" {
  description = "Enable CloudTrail for auditing"
  type        = bool
  default     = true
}

# Common Tags
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Project     = "document-processing"
    ManagedBy   = "terraform"
  }
}
```

Generate variables.tf with dynamic values extracted from customer requirements. Use sensible defaults that can be overridden via terraform.tfvars.
"""
