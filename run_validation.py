#!/usr/bin/env python3
"""
Test script to run only the terraform module validation agent on existing modules.
"""

import os
import sys
from datetime import datetime
from crewai import Task, Crew, Process
from agents.terraform_module_generator import terraform_module_validator_agent

def create_validation_tasks(modules_path, validator_agent):
    """Create validation tasks for all existing modules."""
    validation_tasks = []

    for module_name in os.listdir(modules_path):
        module_path = os.path.join(modules_path, module_name)
        if os.path.isdir(module_path):
            task = Task(
                description=f"""
Validate the Terraform module located at `{module_path}`.
It must contain:
- `main.tf` (AWS resources),
- `variables.tf` (declaring all inputs used),
- `outputs.tf` (exposing useful output values).

Perform the following specific validations:

1. **Variable Declaration Validation:**
   - Confirm that all variables used in `main.tf` are declared in `variables.tf` with appropriate types
   - Check that variable types match their usage (string, number, bool, list, map)
   - Verify that required variables are marked as required or have default values

2. **AWS Resource Type Validation:**
   - Validate that the AWS resource blocks are using correct Terraform resource types (e.g., `aws_vpc`, `aws_subnet`, `aws_instance`, etc.)
   - Check that resource names follow Terraform naming conventions
   - Ensure no typos in resource type names

3. **Resource Configuration Completeness:**
   - Check that the resource configurations are complete (e.g., `aws_vpc` should have a `cidr_block` and `tags`, etc.)
   - Verify that required arguments are provided for each resource
   - Check that optional but recommended arguments are included (like tags)

4. **Output Validation:**
   - Ensure all outputs in `outputs.tf` are referencing valid attributes from resources
   - Check that output names match what's expected by the root-level outputs.tf
   - Verify that referenced resource attributes actually exist

5. **Missing Elements Check:**
   - Suggest improvements or flag any missing elements (e.g., NAT gateway missing when needed, missing availability zones, etc.)
   - Check for common missing components based on module type: For Example:
     - VPC modules: Check for internet gateway, route tables, security groups
     - Compute modules: Check for load balancers, auto scaling groups
     - Database modules: Check for backup configurations, monitoring
     - Security modules: Check for WAF, IAM roles, encryption

6. **Security and Best Practices:**
   - Ensure that the module aligns with security and best practices (e.g., tagging, modularity, flow logs if enabled)
   - Check for proper tagging strategy (Name, Environment, Project tags)
   - Verify encryption settings where applicable
   - Check for proper IAM permissions and least privilege
   - Validate that security groups are properly configured
   - Check for logging and monitoring configurations

Provide a detailed report with:
✅ **Validation Summary** (Pass/Fail for each category)
📋 **Issues Found** (List specific problems with line numbers if possible)
💡 **Suggestions** (Specific improvements and missing elements)
🔧 **Recommended Fixes** (Actionable steps to resolve issues)
📊 **Module Health Score** (Overall assessment of the module quality)

For each validation category, provide specific examples and line references where possible.
""",
                expected_output=f"Comprehensive validation result report for module: {module_name} with detailed analysis of all 6 validation categories",
                agent=validator_agent
            )
            validation_tasks.append(task)
    
    return validation_tasks

def save_validation_results(validation_result, modules_list, modules_dir, output_dir="output"):
    """Save validation results as a markdown file."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create filename
    filename = f"terraform_module_validation_test_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Create markdown content
    md_content = f"""# Terraform Module Validation Test Report

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Modules Validated:** {len(modules_list)}
**Test Type:** Validation-only test

## Summary

- **Modules Directory:** `{modules_dir}`
- **Modules Found:** {', '.join(modules_list)}
- **Validation Status:** {'✅ Completed' if validation_result else '❌ Failed'}

## Validation Results

{validation_result}

## Module Details

"""
    
    # Add individual module information
    for module in modules_list:
        module_path = os.path.join(modules_dir, module)
        if os.path.exists(module_path):
            files = os.listdir(module_path)
            expected_files = ['main.tf', 'variables.tf', 'outputs.tf']
            missing_files = [f for f in expected_files if f not in files]
            
            md_content += f"""
### Module: `{module}`

**Path:** `{module_path}`
**Files Present:** {', '.join(files)}
"""
            
            if missing_files:
                md_content += f"**Missing Files:** {', '.join(missing_files)}\n"
            else:
                md_content += "**Status:** ✅ All required files present\n"
            
            # Check for output blocks in main.tf
            main_tf_path = os.path.join(module_path, "main.tf")
            if os.path.exists(main_tf_path):
                with open(main_tf_path, "r") as f:
                    content = f.read()
                    if "output" in content:
                        md_content += "**Warning:** ⚠️ main.tf contains output blocks\n"
                    else:
                        md_content += "**Status:** ✅ main.tf is clean (no output blocks)\n"
    
    md_content += f"""

## Test Notes

- This report was generated by running only the validation agent on existing modules
- Each module was validated for correct structure, variable declarations, and resource configurations
- Issues and suggestions are included in the validation results above
- This test does not generate new modules, only validates existing ones

---
*Generated by Terraform Module Validation Test*
"""
    
    # Write the file
    try:
        with open(filepath, "w") as f:
            f.write(md_content)
        print(f"✅ Validation results saved to: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving validation results: {e}")
        return None

def test_validation():
    """Test the validation agent on existing modules."""
    
    # Check if modules directory exists
    modules_dir = "modules"
    if not os.path.exists(modules_dir):
        print("❌ Modules directory not found!")
        print(f"Expected path: {modules_dir}")
        print("Please ensure modules exist in the modules/ directory.")
        return
    
    print("🔍 Testing terraform module validation on existing modules...")
    
    # Get list of existing modules
    modules_list = [d for d in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, d))]
    
    if not modules_list:
        print("❌ No modules found in the modules directory!")
        print(f"Directory: {modules_dir}")
        print("Please ensure modules have been generated first.")
        return
    
    print(f"🔍 Found {len(modules_list)} modules to validate: {', '.join(modules_list)}")
    
    # Display module structure
    print("\n📁 Module Structure:")
    for module in modules_list:
        module_path = os.path.join(modules_dir, module)
        files = os.listdir(module_path)
        print(f"   - {module}: {files}")
        
        # Check for output blocks in main.tf
        main_tf_path = os.path.join(module_path, "main.tf")
        if os.path.exists(main_tf_path):
            with open(main_tf_path, "r") as f:
                content = f.read()
                if "output" in content:
                    print(f"     ⚠️  WARNING: {module}/main.tf contains output blocks!")
    
    # Create validation tasks for all existing modules
    print("\n🔍 Creating validation tasks...")
    validation_tasks = create_validation_tasks(modules_dir, terraform_module_validator_agent)
    
    if not validation_tasks:
        print("❌ No validation tasks created!")
        return
    
    print(f"✅ Created {len(validation_tasks)} validation tasks")
    
    # Create validation crew
    validation_crew = Crew(
        agents=[terraform_module_validator_agent],
        tasks=validation_tasks,
        verbose=True,
        process=Process.sequential
    )
    
    # Run validation
    print("\n🚀 Running module validation...")
    validation_result = validation_crew.kickoff()
    
    print("\n✅ Module validation completed!")
    print(f"Validation Result: {validation_result}")
    
    # Save validation results to markdown file
    print("\n💾 Saving validation results...")
    saved_file = save_validation_results(validation_result, modules_list, modules_dir)
    if saved_file:
        print(f"📄 Validation report saved to: {saved_file}")
    
    # Summary
    print(f"\n📊 Validation Test Summary:")
    print(f"   Modules validated: {len(modules_list)} ({', '.join(modules_list)})")
    print(f"   Validation tasks: {len(validation_tasks)}")
    print(f"   Report saved: {'Yes' if saved_file else 'No'}")
    
    return validation_result

if __name__ == "__main__":
    test_validation() 