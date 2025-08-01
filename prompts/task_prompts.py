PARSE_PROMPT = """
You are an AWS infrastructure expert.
Given this request: "{request}"
Extract all AWS resources (VPC, Subnets, EC2, NAT, etc.) and output a structured JSON plan.
"""

PLAN_DEPENDENCY_PROMPT = """
Read the infrastructure JSON plan from output/infra_plan.json and define dependencies and Terraform module layout.
Output a dependency-aware, WAF-aligned JSON with proper resource dependencies and module organization.

Structure the output as follows:

```json
{
  "modules": {
    "vpc": {
      "resources": {
        "aws_vpc": {
          "description": "Description of the VPC resource",
          "dependencies": [],
          "waf_considerations": {
            "security": "Enable flow logs to monitor network traffic.",
            "reliability": "Design with multiple subnets in different AZs for fault tolerance.",
            "cost_optimization": "Avoid unused CIDR blocks to minimize wasted IPs."
          }
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
          "dependencies": ["aws_subnet", "aws_security_group"],
          "waf_considerations": {
            "security": "Ensure instance roles follow least privilege principle.",
            "operational_excellence": "Use EC2 instance recovery alarms.",
            "performance_efficiency": "Right-size instances based on expected workload."
          }
        }
      }
    }
  }
}
```

Key requirements:
1. Extract actual resources from the output/infra_plan.json file
2. Organize by logical modules (vpc, compute, storage, database, security, monitoring, etc.)
3. Each resource should have a clear description
4. List dependencies as resource names (e.g., "aws_vpc", "aws_subnet")
5. Use empty array [] for resources with no dependencies
6. Focus on the specific infrastructure components mentioned in the plan
7. Where applicable, annotate each resource with AWS Well-Architected Framework best practices under the waf_considerations field. Focus on relevant pillars such as:
    - Security (e.g., encryption, IAM, traffic restrictions)
    - Reliability (e.g., multi-AZ, failover)
    - Operational Excellence (e.g., monitoring, automation)
    - Cost Optimization (e.g., sizing, lifecycle policies)
    - Performance Efficiency (e.g., autoscaling, right sizing)
    - Sustainability (e.g., cleanup policies, efficient compute)
"""

GENERATE_PROMPT = """
Take the dependency-aware infrastructure plan and customer requirements to generate comprehensive Terraform HCL code using a MODULAR approach.

IMPORTANT:
- Extract ALL parameters dynamically from the customer requirements instead of hardcoding values.
- Use the waf_considerations field to embed AWS Well-Architected Framework best practices directly into module parameters (e.g., enable monitoring, encryption, autoscaling, backups).

Generate a main.tf file (only valid HCL code, no text or comments outside HCL) using module blocks for each major component detected in the infrastructure plan, with dynamically extracted parameters.

Modules to include (examples, generate only those relevant):
- Provider: provider "aws" { ... }
- VPC Module: module "vpc" { ... }
- Security Module: module "security" { ... }
- Compute Module: module "compute" { ... }
- Storage Module: module "storage" { ... }
- Database Module: module "database" { ... }
- Monitoring Module: module "monitoring" { ... }
- Cost Management Module: module "cost_management" { ... }
- Scalability Module: module "scalability" { ... }
- Backup Module: module "backup" { ... }
- FinOps Module: module "finops" { ... }

Module Requirements:
- Use source = "./modules/<module_name>"
- Reference outputs from other modules where applicable (e.g., vpc_id, subnet_ids, security_group_id)
- All values must come from customer requirements (e.g., number of EC2s, budget amount, enable encryption, etc.)
- Use Terraform variables (var.*) for all dynamic values
- Ensure tags are included (tags = var.common_tags) for cost and operational visibility
- Do not use root-level resource blocks — only use module blocks
- Embed waf_considerations as real module input parameters (e.g., encryption_enabled = true, enable_monitoring = true, backup_retention_days = 7)

CRITICAL WAF IMPLEMENTATION REQUIREMENTS:
You MUST convert waf_considerations from the JSON file into actual module parameters:

EXAMPLES such as
1. VPC Module - Add these parameters based on waf_considerations:
   - enable_flow_logs = true (from security consideration)
   - multi_az_deployment = true (from reliability consideration)
   - single_nat_gateway = true (from cost optimization)

2. Compute Module - Add these parameters based on waf_considerations:
   - enable_instance_recovery = true (from operational excellence)
   - enable_autoscaling = true (from performance efficiency)
   - enable_right_sizing = true (from performance efficiency)

3. Storage Module - Add these parameters based on waf_considerations:
   - enable_encryption = true (from security)
   - enable_access_logging = true (from security)
   - enable_lifecycle_policies = true (from cost optimization)

4. Database Module - Add these parameters based on waf_considerations:
   - enable_encryption_at_rest = true (from security)
   - enable_encryption_in_transit = true (from security)
   - enable_multi_az = true (from reliability)
   - enable_backups = true (from reliability)

5. Monitoring Module - Add these parameters based on waf_considerations:
   - enable_critical_alarms = true (from operational excellence)
   - enable_log_validation = true (from security)

Output Instructions:
- Output a complete and valid main.tf and outputs.tf in HCL format.
- Do not include any comments or text outside HCL code.
- All module blocks must be fully defined in main.tf.
- All output blocks must be fully defined in outputs.tf.
- Parameters must be populated via variables (e.g., var.ami_id, var.budget_amount).
- WAF-aligned parameters must be embedded based on waf_considerations (monitoring, encryption, backups, cost alerts, etc.).
- Include output blocks for all key values (e.g., VPC ID, EC2 IDs, S3 name, RDS endpoint).
- Format the output as follows:

```hcl
// main.tf
[All module blocks here]

// outputs.tf
[All output blocks here]
```

- The combined file should be created in the output/final/terraform/ directory as main.tf.
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

DYNAMIC TASK CATEGORY GENERATION:
Do NOT use hardcoded task categories. Instead, analyze the customer requirements and generate task categories based on what's actually needed:

1. **Analyze Customer Requirements:**
   - Identify all mentioned AWS services and components
   - Determine infrastructure categories based on actual needs
   - Consider business requirements, technical requirements, and constraints

2. **Generate Task Categories Dynamically:**
   - Create categories only for infrastructure components that are actually mentioned
   - Use descriptive category names based on the actual requirements
   - Include categories for any special requirements (compliance, security, etc.)
   - Add FinOps/cost optimization categories if budget constraints are mentioned

3. **Example Dynamic Categories** (generate based on actual requirements):
   - If VPC/networking mentioned → "VPC and Networking Setup"
   - If EC2/Lambda mentioned → "Compute Resources"
   - If S3/EBS mentioned → "Storage and Database"
   - If security/compliance mentioned → "Security and Compliance"
   - If monitoring/logging mentioned → "Monitoring and Logging"
   - If budget/cost mentioned → "Cost Optimization and FinOps"
   - If backup/disaster recovery mentioned → "Backup and Disaster Recovery"
   - If testing/validation mentioned → "Testing and Validation"
   - If any other specific requirements → create appropriate categories

Output a detailed planning document in markdown format with the following structure:

# AWS Infrastructure Implementation Plan

## Project Overview
[Brief project description and objectives]

## Infrastructure Categories and Tasks

[Dynamically generate task categories based on actual customer requirements]
[For each category, generate numbered tasks such as 1.1, 1.2, 1.3, etc. based on actual requirements including dependencies and complexity]
[Ensure all tasks level dependencies are included in this section as "Task 1.1,Task 2.3" etc., Keep empty if no dependencies exists]

## Dependencies and Timeline
[Outline high level dependencies and estimated timeline based on actual requirements]

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
syntax with clear node definitions and meaningful relationships. **IMPORTANT: Avoid circular references by using
proper hierarchical relationships. Do NOT create cycles (circular dependencies) in the diagram, as these will cause rendering errors.**

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
8. WAF Alignment Considerations for each component:
   - Security considerations (e.g., Data protection, identity and access, infrastructure security, etc.)
   - Reliability considerations (e.g., Auto scaling, multi-AZ architecture, fault tolerance, backups, Route 53, etc.)
   - Operational Excellence considerations (e.g., monitoring, automation, etc.)
   - Performance Efficiency considerations (e.g., autoscaling, right sizing,storage, databases, caching, CDN-CloudFront, etc.)
   - Cost Optimization considerations (e.g., sizing, lifecycle policies, cost allocation, tagging, etc.)

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

DYNAMIC REQUIREMENTS STRUCTURE GENERATION:
Do NOT use hardcoded requirement sections. Instead, analyze the customer intent and generate requirement sections based on what's actually needed:

1. **Analyze Customer Intent:**
   - Identify all mentioned business needs and technical requirements
   - Determine which AWS services are relevant
   - Understand performance, security, and compliance needs
   - Identify cost constraints and optimization opportunities

2. **Generate Requirement Sections Dynamically:**
   - Create sections only for requirements that are actually mentioned
   - Use descriptive section names based on actual business needs
   - Include sections for any special requirements (compliance, security, etc.)
   - Add cost optimization sections if budget constraints are mentioned

3. **Example Dynamic Sections** (generate based on actual intent):
   - If compute needs mentioned → "Compute Requirements"
   - If storage needs mentioned → "Storage Requirements"
   - If database needs mentioned → "Database Requirements"
   - If networking needs mentioned → "Networking Requirements"
   - If security needs mentioned → "Security & Compliance Requirements"
   - If monitoring needs mentioned → "Monitoring & Observability Requirements"
   - If cost constraints mentioned → "Cost Optimization Requirements"
   - If integration needs mentioned → "Integration & Connectivity Requirements"
   - If any other specific needs → create appropriate sections

Output a comprehensive AWS requirements document in markdown format with the following structure:

# AWS Infrastructure Requirements

## Business Overview
[Brief description of the business context and objectives]

## Technical Requirements

[Dynamically generate requirement sections based on actual customer intent]

### Example Dynamic Sections (replace with actual requirements):
- **Compute Requirements**: [EC2, Lambda, ECS, etc.] [if compute needs mentioned]
- **Storage Requirements**: [S3, EBS, EFS, etc.] [if storage needs mentioned]
- **Database Requirements**: [RDS, DynamoDB, ElastiCache, etc.] [if database needs mentioned]
- **Networking Requirements**: [VPC, subnets, load balancers, etc.] [if networking needs mentioned]

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
Generate a comprehensive variables.tf file based on the customer requirements, infrastructure plan, and WAF considerations from the infra_plan_with_dependencies.json file.

IMPORTANT:
- Extract ALL parameters dynamically from the customer requirements instead of hardcoding values.
- Dynamically extract WAF considerations from the infra_plan_with_dependencies.json file and convert them into Terraform variables.
- Do NOT hardcode specific variable names - instead, analyze the JSON structure and create variables based on the actual waf_considerations present.
- Do NOT assume specific variable categories - extract variables based on what the customer actually needs.

DYNAMIC VARIABLE EXTRACTION PROCESS:

1. **Analyze Customer Requirements:**
   - Read the customer requirements document
   - Identify all mentioned infrastructure components (VPC, EC2, S3, RDS, etc.)
   - Extract specific values mentioned (budget amounts, instance counts, regions, etc.)
   - Identify security, compliance, and operational requirements

2. **Analyze Infrastructure Plan:**
   - Read the infrastructure plan JSON
   - Identify all planned AWS resources
   - Extract resource-specific parameters and configurations
   - Identify dependencies and relationships

3. **Analyze WAF Considerations:**
   - Read the infra_plan_with_dependencies.json file
   - Look for "waf_considerations" in each resource
   - Extract ALL WAF pillars (security, reliability, operational_excellence, performance_efficiency, cost_optimization)
   - Convert EACH AND EVERY WAF consideration into appropriate Terraform variables
   - DO NOT skip any WAF consideration - extract ALL of them
   - For each resource, check ALL waf_considerations and create variables for each one

4. **Generate Variables Dynamically:**
   - Create variables only for what's actually needed based on requirements
   - Use descriptive names based on actual requirements
   - Set appropriate types and default values
   - Include clear descriptions linking to the original requirement

Examples of dynamic extraction (DO NOT hardcode these - use as examples only):
- If customer mentions "2 EC2 instances" → create variable "instance_count" with default = 2
- If customer mentions "$200/month budget" → create variable "budget_amount" with default = 200
- If customer mentions "us-west-2 region" → create variable "aws_region" with default = "us-west-2"
- If JSON has "security": "Enable flow logs" → create variable "waf_enable_flow_logs" with default = true
- If JSON has "reliability": "Multi-AZ deployment" → create variable "waf_multi_az_deployment" with default = true
- If JSON has "security": "Use NACLs to control traffic" → create variable "waf_enable_nacls" with default = true
- If JSON has "performance_efficiency": "Right-size instances" → create variable "waf_right_size_instances" with default = true
- If JSON has "cost_optimization": "Use lifecycle policies" → create variable "waf_enable_lifecycle_policies" with default = true

CRITICAL REQUIREMENT: Extract ALL WAF considerations from ALL resources. Do not miss any single WAF consideration.

Generate variables.tf with proper descriptions and default values:

```hcl
# Dynamically generated variables based on customer requirements
# [Generate variables based on actual requirements found in customer documents]

# Example format (replace with actual extracted variables):
# variable "project_name" {
#   description = "Name of the project extracted from requirements"
#   type        = string
#   default     = "[EXTRACT FROM CUSTOMER REQUIREMENTS]"
# }

# variable "instance_count" {
#   description = "Number of EC2 instances (extracted from requirements)"
#   type        = number
#   default     = [EXTRACT FROM REQUIREMENTS]
# }

# variable "budget_amount" {
#   description = "Monthly budget amount (extracted from requirements)"
#   type        = number
#   default     = [EXTRACT FROM BUDGET REQUIREMENTS]
# }

# WAF-Specific Variables (dynamically extracted from waf_considerations)
# [Generate variables based on actual waf_considerations found in the infra_plan_with_dependencies.json file]
# Example format:
# variable "waf_enable_flow_logs" {
#   description = "Enable VPC flow logs for network traffic monitoring (WAF Security)"
#   type        = bool
#   default     = true
# }

# Common Tags (extract from tagging requirements)
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  default = {
    Environment = "[EXTRACT FROM ENVIRONMENT REQUIREMENTS]"
    Project     = "[EXTRACT FROM PROJECT REQUIREMENTS]"
    ManagedBy   = "terraform"
  }
}
```

Generate variables.tf with dynamic values extracted from customer requirements AND dynamically extracted WAF considerations from the infra_plan_with_dependencies.json file. Use sensible defaults that can be overridden via terraform.tfvars.
"""
