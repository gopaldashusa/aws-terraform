#!/usr/bin/env python3
"""
AWS Terraform Modules Generator - Demo Application

A focused demonstration of the Terraform Module Generator that transforms existing Terraform 
main.tf files into modular, production-ready Terraform module structures.
This demo showcases the module generation and validation workflow.
"""

import os
import sys
import subprocess
from tools.show_requirements import show_markdown
from tools.prepostcheck import run_pre_checks, run_post_activities


def print_banner():
    """Print a professional welcome banner for the modules demo"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                    🏗️ AWS Terraform Modules Generator - Demo Application                              ║
║                                                                                                        ║
║  A specialized system that transforms monolithic Terraform configurations into modular,               ║
║  production-ready Terraform module structures with comprehensive validation.                          ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    input("\n⏸️  Press Enter to start the modules demo...")

def show_system_features():
    """Display the module generation system features and capabilities"""
    print("🎯 STEP 1: Terraform Modules Generator Overview")
    print("=" * 100)
    
    # Section 1: Key Features
    print("\n🚀 **Key Features**")
    print("-" * 50)
    features1 = """
• Module Extraction        → Analyze existing main.tf to identify module requirements
• Intelligent Generation   → Create complete module structures with proper separation
• Variable Preservation   → Maintain exact variable names and default values
• Comprehensive Validation → Multi-category validation with detailed reporting
• Production-Ready Output → Generate modular, maintainable Terraform code
• Documentation           → Detailed validation reports and module health scores
    """
    print(features1)
    input("\n⏸️  Press Enter to continue to Module Structure...")
    
    # Section 2: Module Structure Overview
    print("\n🏗️ **Module Structure Overview**")
    print("-" * 50)
    structure = """
Each generated module follows Terraform best practices with three essential files:

```
modules/<module_name>/
├── main.tf      (AWS resources and configurations)
├── variables.tf (Input variable declarations)
└── outputs.tf   (Output value definitions)
```
    """
    print(structure)
    input("\n⏸️  Press Enter to continue to AI Agent Workflow...")
    
    # Section 3: AI Agent Workflow
    print("\n🤖 **AI Agent Workflow**")
    print("-" * 50)
    agents = """
1. **Terraform Module Generator** → Analyzes main.tf and creates modular structure
2. **Terraform Module Validator** → Comprehensive validation across 6 categories:
   • Variable Declaration Validation
   • AWS Resource Type Validation  
   • Resource Configuration Completeness
   • Output Validation
   • Missing Elements Check
   • Security and Best Practices
    """
    print(agents)
    input("\n⏸️  Press Enter to continue to Validation Categories...")
    
    # Section 4: Validation Categories
    print("\n📊 **Validation Categories**")
    print("-" * 50)
    validation = """
**Variable Declaration:** Confirm all variables are properly declared with correct types
**AWS Resource Types:** Validate correct Terraform resource types and naming conventions
**Configuration Completeness:** Check required arguments and recommended configurations
**Output Validation:** Ensure outputs reference valid resource attributes
**Missing Elements:** Identify common missing components based on module type
**Security & Best Practices:** Verify tagging, encryption, IAM, and monitoring configurations
    """
    print(validation)
    input("\n⏸️  Press Enter to continue to Technologies...")
    
    # Section 5: Technologies & Tools
    print("\n🛠️ **Technologies & Tools**")
    print("-" * 50)
    tech = """
• CrewAI              → Multi-Agent Framework for orchestration
• OpenAI GPT Models   → Intelligent module generation and validation
• Terraform HCL       → Infrastructure as Code configuration
    """
    print(tech)
    input("\n⏸️  Press Enter to continue to Prerequisites...")
     
def check_prerequisites():
    """Check if required files exist and display current state"""
    print("\n📋 STEP 2: Prerequisites Check")
    print("=" * 100)
    
    required_files = [
        "output/final/terraform/main.tf",
        "output/final/terraform/variables.tf", 
        "output/final/terraform/outputs.tf"
    ]
    
    print("🔍 Checking for required Terraform files...")
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️  Missing required files: {len(missing_files)}")
        print("   The following files are required to run the module generator:")
        for file in missing_files:
            print(f"   • {file}")
        print("\n💡 Please run the full workflow first to generate these files.")
        return False
    
    print(f"\n✅ All required files found!")
    
    # Show file sizes for context
    print("\n📊 File Information:")
    for file_path in required_files:
        size = os.path.getsize(file_path)
        print(f"   • {file_path}: {size:,} bytes")
    
    # Wait for user confirmation
    while True:
        response = input("\n❓ Do you want to proceed with module generation? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("✅ Proceeding with module generation...")
            input("\n⏸️  Press Enter to continue to Step 3...")
            return True
        elif response in ['n', 'no']:
            print("❌ Demo cancelled by user.")
            return False
        else:
            print("⚠️  Please enter 'y' or 'n'")

def run_module_generation():
    """Execute the module generation workflow"""
    print("\n🚀 STEP 3: Executing Module Generation")
    print("=" * 100)
    print("🔄 Starting Terraform module generation process...")
    
    try:
        # Import and run the module generator
        from generate_terraform_modules import module_generator
        result = module_generator()
        return True
    except Exception as e:
        print(f"❌ Error during module generation: {e}")
        return False

def show_thank_you_message():
    """Display thank you message with module generation summary"""
    print("\n🎉 STEP 4: Demo Complete - Thank You!")
    print("=" * 100)
    
    thank_you_message = """
🎯 **Module Generation Summary**

The system successfully executed the Terraform Module Generator workflow:

📁 **Generated Outputs**

**Modular Structure:** Complete Terraform modules with proper separation
**Validation Reports:** Comprehensive validation with health scores
**Documentation:** Detailed analysis of each module's quality and completeness

**Next Steps:**
• Review generated modules in `output/final/terraform/modules/`
• Check validation reports for any issues or improvements
• Customize modules as needed for your specific requirements
• Deploy using standard Terraform commands

Thank you for experiencing the AWS Terraform Modules Generator!
    """
    
    print(thank_you_message)
    print("=" * 100)
    input("\n⏸️  Press Enter to exit the demo...")

def main():
    """Main demo function with comprehensive error handling"""
    try:        
        # Step 1: Show system features
        print_banner()
        show_system_features()
        
        # Step 2: Check prerequisites and get confirmation
        if not check_prerequisites():
            print("\n👋 Demo ended. Goodbye!")
            return
        
        # Step 3: Run module generation
        success = run_module_generation()
        
        # Step 4: Show thank you message
        show_thank_you_message()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error during demo: {e}")
        print("💡 Please check the error message and try again.")

if __name__ == "__main__":
    main() 