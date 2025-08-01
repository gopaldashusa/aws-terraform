# AWS Infrastructure Automation with CrewAI

A sophisticated multi-agent system that transforms natural language customer requirements into production-ready AWS infrastructure using Terraform. This project leverages CrewAI to orchestrate specialized agents that handle everything from business analysis to infrastructure code generation.

## 🚀 Features

- **Natural Language Processing**: Convert customer intent into detailed AWS requirements
- **Multi-Agent Workflow**: Specialized agents for each phase of infrastructure planning
- **Cost Optimization**: Built-in FinOps practices and cost management
- **Visual Architecture**: Automatic generation of architecture diagrams
- **Production-Ready Code**: Generate modular, dependency-aware Terraform configurations
- **Comprehensive Documentation**: Planning, design, and technical specifications

## 🏗️ Architecture

The system uses a 5-agent workflow to transform requirements into infrastructure:

```
Customer Intent → Requirements → Planning → Design → Technical Specs → Terraform Code
```

### Agent Workflow

1. **Customer Intent Parser** - Transforms natural language into AWS-specific requirements
2. **Customer Requirement Parser** - Creates detailed planning and design documents with FinOps focus
3. **Technical Requirement Parser** - Extracts AWS resources into structured JSON
4. **Terraform Planner** - Defines dependencies and module organization
5. **Terraform Generator** - Produces production-ready HCL code

## 📁 Project Structure

```
aws-terraform/
├── agents/                          # CrewAI agent definitions
│   ├── customer_intent_parser.py
│   ├── customer_req_parser.py
│   ├── technical_req_parser.py
│   ├── terraform_planner.py
│   └── terraform_generator.py
├── tasks/                           # Task definitions
│   └── tasks.py
├── prompts/                         # Agent prompts and templates
│   └── task_prompts.py
├── tools/                           # Utility tools
│   ├── mermaid_converter.py
│   └── white_background.css
├── input/                           # Input files
│   └── customer_intent.md
├── output/                          # Generated outputs
│   ├── customer_requirement.md
│   ├── infra_plan.json
│   ├── infra_plan_with_dependencies.json
│   └── final/                       # Final deliverables
│       ├── planning_output.md
│       ├── design_output.md
│       ├── architecture_diagram.png
│       └── main.tf
├── main.py                          # Main execution script
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Node.js (for Mermaid CLI)
- AWS CLI (optional, for deployment)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd aws-terraform
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Mermaid CLI** (for diagram generation)
   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your OpenAI API key and model preferences
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o
```

### Input Requirements

Create `input/customer_intent.md` with your infrastructure requirements:

```markdown
# Customer Intent

We need a document processing system with the following requirements:
- Store documents securely in S3
- Process documents using EC2 instances
- Store metadata in RDS database
- Budget constraint: $200/month
- Must be GDPR compliant
- High availability requirements
```

## 🚀 Usage

### Quick Start

1. **Prepare your requirements**
   ```bash
   # Edit input/customer_intent.md with your infrastructure needs
   nano input/customer_intent.md
   ```

2. **Run the automation**
   ```bash
   python3 main.py
   ```

3. **Review outputs**
   - Check `output/final/` for all deliverables
   - Review `architecture_diagram.png` for visual representation
   - Examine `main.tf` for Terraform code

### Manual Diagram Generation

To regenerate the architecture diagram:

```bash
python3 tools/mermaid_converter.py output/final/design_output.md --output-dir output/final
```

## 📊 Outputs

The system generates comprehensive outputs:

### Documentation
- **`customer_requirement.md`** - Detailed AWS-specific requirements
- **`planning_output.md`** - Project planning with tasks and dependencies
- **`design_output.md`** - Architecture design with Mermaid diagram

### Technical Specifications
- **`infra_plan.json`** - Structured AWS resource definitions
- **`infra_plan_with_dependencies.json`** - Dependency-aware infrastructure plan
  - Dependency mapping for proper resource creation order
  - WAF best practices embedded in each resource
  - Modular structure aligned with Terraform modules
  - Technical specifications needed for actual implementation


### Final Deliverables
- **`architecture_diagram.png`** - Visual architecture diagram
- **`main.tf`** - Production-ready Terraform configuration

## 🎯 Agent Capabilities

### Customer Intent Parser
- Transforms natural language into technical requirements
- Identifies AWS services and architectural patterns
- Bridges business needs and technical implementation

### Customer Requirement Parser
- Creates detailed planning documents
- Applies FinOps best practices
- Includes cost optimization strategies
- Generates Mermaid architecture diagrams

### Technical Requirement Parser
- Extracts AWS resources from planning documents
- Creates structured JSON specifications
- Maps business requirements to technical components

### Terraform Planner
- Defines resource dependencies
- Organizes infrastructure into modules
- Plans deployment order and relationships

### Terraform Generator
- Generates production-ready HCL code
- Includes security, monitoring, and cost management
- Creates modular, maintainable configurations

## 💰 Cost Optimization Features

The system includes comprehensive FinOps practices:

- **Right-sizing recommendations** for EC2 instances
- **Cost allocation and tagging** strategies
- **Budget monitoring and alerting** setup
- **Reserved Instance/Savings Plan** recommendations
- **Auto-scaling policies** for cost optimization
- **Storage optimization** strategies
- **Network cost optimization**
- **Monthly cost estimates** and breakdown

## 🔒 Security & Compliance

- **Data encryption** at rest and in transit
- **IAM roles** with least privilege principle
- **Security groups** and Network ACLs
- **GDPR compliance** considerations
- **AWS security best practices**

## 🎨 Customization

### Modifying Agent Behavior

Edit agent files in `agents/` to customize:
- Agent roles and goals
- Backstory and expertise
- Temperature settings for creativity

### Updating Prompts

Modify `prompts/task_prompts.py` to:
- Change output formats
- Add new requirements
- Customize analysis depth

### Diagram Styling

Adjust `tools/white_background.css` to:
- Change font sizes
- Modify colors and spacing
- Customize visual appearance

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify API key in `.env`
   - Check API quota and billing
   - Ensure model name is correct

2. **Mermaid Diagram Issues**
   - Verify Mermaid CLI installation: `mmdc --version`
   - Check CSS file permissions
   - Ensure output directory exists

3. **Import Errors**
   - Install all dependencies: `pip install -r requirements.txt`
   - Check Python version compatibility
   - Verify file paths and structure

### Debug Mode

Enable verbose output by setting `verbose=True` in agent configurations.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **CrewAI** for the multi-agent framework
- **OpenAI** for the language models
- **Mermaid** for diagram generation
- **HashiCorp** for Terraform

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the documentation

---

**Built with ❤️ using CrewAI and OpenAI**
