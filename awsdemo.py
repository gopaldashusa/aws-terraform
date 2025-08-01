#!/usr/bin/env python3
"""
AWS Infrastructure Automation with CrewAI - Demo Application

A comprehensive demonstration of the sophisticated multi-agent system that transforms 
natural language customer requirements into production-ready AWS infrastructure using Terraform.
This demo showcases the complete workflow from business analysis to infrastructure code generation.
"""

import os
import sys
import subprocess
from tools.show_requirements import show_markdown
from tools.prepostcheck import run_pre_checks, run_post_activities


def print_banner():
    """Print a professional welcome banner for the demo"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                    🚀 AWS Infrastructure Automation with CrewAI                                        ║
║                              Demo Application                                                          ║
║                                                                                                        ║
║  A sophisticated multi-agent system that transforms natural language customer requirements into        ║
║  production-ready AWS infrastructure using Terraform.                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    input("\n⏸️  Press Enter to start the demo...")

def show_system_features():
    """Display the system features and capabilities in smaller, digestible sections"""
    print("🎯 STEP 1: System Features Overview")
    print("=" * 100)
    
    # Section 1: Key Features
    print("\n🚀 **Key Features**")
    print("-" * 50)
    features1 = """
• Natural Language Processing → Convert customer intent into AWS requirements document
• Multi-Agent Workflow        → Specialized agents for each stage of the AWS infrastructure implementation process
• Visual Architecture         → Automatic generation of architecture diagrams
• Production-Ready Code       → Generate modular, dependency-aware Terraform configurations
• Documentation               → Planning, design, and technical specifications
    """
    print(features1)
    input("\n⏸️  Press Enter to continue to Architecture Overview...")
    
    # Section 2: Architecture Overview
    print("\n🏗️ **Architecture Overview**")
    print("-" * 50)
    architecture = """
The system uses a sophisticated 6-agent workflow to transform requirements into infrastructure as code:

```
Customer Intent → Requirements → Planning → Tech Arch & Design → Infrastructure Plan → Terraform Code
```
    """
    print(architecture)
    input("\n⏸️  Press Enter to continue to AI Agent Workflow...")
    
    # Section 3: AI Agent Workflow
    print("\n🤖 **AI Agent Workflow**")
    print("-" * 50)
    agents = """
1. **Customer Intent Parser**       → Transforms natural language into AWS-specific requirements
2. **Customer Requirement Parser**  → Creates detailed planning documents with FinOps focus
3. **Technical Requirement Parser** → Extracts AWS resources into structured JSON
4. **Terraform Planner**            → Defines resource dependencies and relationships
5. **Terraform Generator**          → Produces production-ready HCL code
6. **Terraform Module Generator**   → Creates complete modular Terraform structure
    """
    print(agents)
    input("\n⏸️  Press Enter to continue to Output Generation...")
    
    # Section 4: Output Generation
    print("\n📊 **Output Generation**")
    print("-" * 50)
    outputs = """
**Documentation:            ** Customer Requirements, Infrastructure Planning, Architecture Design
**Technical Specifications: ** Structured JSON plans with dependencies
**Final Deliverables:       ** Terraform Configuration Files, Modular Structure, Visual Diagrams
    """
    print(outputs)
    input("\n⏸️  Press Enter to continue to Technologies...")
    
    # Section 5: Technologies & Tools
    print("\n🛠️ **Technologies & Tools**")
    print("-" * 50)
    tech = """
• CrewAI              → Multi-Agent Framework for orchestration
• OpenAI GPT Models   → Natural Language Processing and code generation
• Terraform HCL       → Infrastructure as Code configuration
• AWS Cloud Services  → Target infrastructure platform
• Mermaid             → Architecture diagram generation
• Python 3.11+        → Backend processing and automation
• FileWriterTool      → File system operations and output generation
• Markdown Processing → Documentation and requirement parsing
    """
    print(tech)
    input("\n⏸️  Press Enter to continue to Cost Optimization...")
     
def show_requirements():
    """Display the current requirements and wait for user confirmation"""
    print("\n📋 STEP 2: Current Infrastructure Requirements")
    print("=" * 100)
    show_markdown("input/customer_intent.md")       
    # Wait for user confirmation
    while True:
        response = input("\n❓ Do you want to proceed with these requirements? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("✅ Proceeding with the workflow...")
            input("\n⏸️  Press Enter to continue to Step 3...")
            return True
        elif response in ['n', 'no']:
            print("❌ Demo cancelled by user.")
            return False
        else:
            print("⚠️  Please enter 'y' or 'n'")

def run_main_workflow():
    """Execute the main workflow"""
    print("\n🚀 STEP 3: Executing Main Workflow")
    print("=" * 100)
    print("🔄 Starting multi-agent infrastructure generation process...")
    
    try:
        # Import and run the main workflow
        from main import main
        main()
        return True
    except Exception as e:
        print(f"❌ Error during workflow execution: {e}")
        return False

def show_thank_you_message():
    """Display thank you message with comprehensive workflow and technology summary"""
    print("\n🎉 STEP 4: Demo Complete - Thank You!")
    print("=" * 100)
    
    thank_you_message = """
🎯 **Agent Workflow Summary**

The system successfully executed a sophisticated 6-agent workflow:

📁 **Generated Outputs**

**Documentation:** Infrastructure planning documents with detailed specifications
**Terraform Configuration:** Modular Terraform structure with separate modules
**Visual Assets:** Visual architecture diagrams in PNG format


Thank you for experiencing the AWS Infrastructure Automation with CrewAI!
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
        
        # Step 2: Show requirements and get confirmation
        if not show_requirements():
            print("\n👋 Demo ended. Goodbye!")
            return
        
        # Step 3: Run main workflow
        success = run_main_workflow()
        
        # Step 4: Show thank you message
        # if success:
        show_thank_you_message()
        # else:
        #     print("\n❌ Workflow execution failed. Please check the logs above.")
        #     print("💡 Common troubleshooting steps:")
        #     print("   • Verify OpenAI API key in .env file")
        #     print("   • Check input/customer_intent.md exists and is valid")
        #     print("   • Ensure all dependencies are installed")
        #     print("   • Review error messages for specific issues")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error during demo: {e}")
        print("💡 Please check the error message and try again.")

if __name__ == "__main__":
    main() 