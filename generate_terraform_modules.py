#!/usr/bin/env python3
"""
Test script to run just the terraform module generator agent with AI prompt and FileWriterTool.
"""

import os
import sys
import re
from datetime import datetime
from crewai import Task, Crew, Process
from agents.terraform_module_generator import terraform_module_generator_agent, terraform_module_validator_agent
from crewai_tools import FileWriterTool

def extract_modules_from_main_tf(main_tf_content):
    """Extract all module names from main.tf content."""
    module_pattern = r'module\s+"([^"]+)"\s*{'
    modules = re.findall(module_pattern, main_tf_content)
    return modules

def create_validation_tasks(modules_path, validator_agent):
    """Create validation tasks for all generated modules."""
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

def save_validation_results(validation_result, created_modules, modules_dir, output_dir="output"):
    """Save validation results as a markdown file."""
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Create filename
    filename = f"terraform_module_validation_{timestamp}.md"
    filepath = os.path.join(output_dir, filename)
    
    # Create markdown content
    md_content = f"""# Terraform Module Validation Report

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Total Modules Validated:** {len(created_modules)}

## Summary

- **Modules Directory:** `{modules_dir}`
- **Modules Found:** {', '.join(created_modules)}
- **Validation Status:** {'✅ Completed' if validation_result else '❌ Failed'}

## Validation Results

{validation_result}

## Module Details

"""
    
    # Add individual module information
    for module in created_modules:
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

## Validation Notes

- This report was generated automatically by the Terraform Module Validator
- Each module was validated for correct structure, variable declarations, and resource configurations
- Issues and suggestions are included in the validation results above

---
*Generated by AWS Terraform Module Generator*
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

def module_generator():
    """Generate the terraform modules."""
    
    # Check if required files exist
    if not os.path.exists("output/final/terraform/main.tf"):
        print("❌ main.tf not found!")
        print("Please run the full workflow first to generate this file.")
        return
    
    if not os.path.exists("output/final/terraform/variables.tf"):
        print("❌ variables.tf not found!")
        print("Please run the full workflow first to generate this file.")
        return
    
    if not os.path.exists("output/final/terraform/outputs.tf"):
        print("❌ outputs.tf not found!")
        print("Please run the full workflow first to generate this file.")
        return
    
    print("🔍 Testing terraform module generator with AI prompt...")
    
    # Clean up existing modules for consistency
    modules_dir = "output/final/terraform/modules"
    if os.path.exists(modules_dir):
        print(f"🧹 Cleaning existing modules in {modules_dir}...")
        import shutil
        shutil.rmtree(modules_dir)
        print(f"✅ Cleaned existing modules")
    
    # Read the existing terraform files to include in the prompt
    with open("output/final/terraform/main.tf", "r") as f:
        main_tf_content = f.read()
    
    with open("output/final/terraform/variables.tf", "r") as f:
        variables_tf_content = f.read()
    
    with open("output/final/terraform/outputs.tf", "r") as f:
        outputs_tf_content = f.read()
    
    print(f"📄 Main.tf content length: {len(main_tf_content)} characters")
    print(f"📄 Variables.tf content length: {len(variables_tf_content)} characters")
    print(f"📄 Outputs.tf content length: {len(outputs_tf_content)} characters")
    
    # Extract all modules from main.tf
    modules = extract_modules_from_main_tf(main_tf_content)
    print(f"🔍 Found {len(modules)} modules: {', '.join(modules)}")
    
    # Create the module generation task with AI prompt
    module_task = Task(
        description=f"""
You are given a `main.tf` file that contains multiple module blocks. Your task is to generate the actual implementation of ALL modules under the folder `output/final/terraform/modules/<module_name>/`.

Here is the root-level main.tf content:
```hcl
{main_tf_content}
```

Here is the variables.tf content:
```hcl
{variables_tf_content}
```

Here is the outputs.tf content:
```hcl
{outputs_tf_content}
```

The modules found in main.tf are: {', '.join(modules)}

CRITICAL: You MUST preserve the exact variable names as they appear in the main.tf module blocks. Do NOT change or rename variables. Use the exact same variable names that are passed to each module in the main.tf file.

PRESERVE DEFAULTS: When creating variables.tf files for modules, preserve the default values from the root-level variables.tf file wherever applicable. Copy the exact default values to maintain consistency.

The root-level `variables.tf` already declares the input variables passed into the modules. You may assume those values are defined and should be re-declared inside each module with the correct types.

The root-level `outputs.tf` exposes module outputs. Ensure each module you're generating exposes matching `output` blocks so that they can be used at the root level.

IMPORTANT: You must create files ONE AT A TIME using the FileWriterTool. For each module, create the three files separately:
1. First create the main.tf file for the module, DO NOT include any output blocks in the main.tf file.
2. Then create the variables.tf file for the module  
3. Finally create the outputs.tf file for the module
4. Repeat for each module

Specifically, your job is to:
1. For EACH module found in main.tf ({', '.join(modules)}), create the corresponding `output/final/terraform/modules/<module_name>/main.tf` containing real AWS Terraform resources that implement the logic implied by the module input variables.
2. For EACH module, create a `output/final/terraform/modules/<module_name>/variables.tf` file that re-declares all variables used in that module's main.tf with the correct types, based on the root-level variable definitions. USE THE EXACT VARIABLE NAMES from the main.tf module blocks. PRESERVE THE EXACT DEFAULT VALUES from the root-level variables.tf file.
3. For EACH module, create an `output/final/terraform/modules/<module_name>/outputs.tf` file to expose useful output values like IDs or ARNs from resources created, ensuring they match the outputs expected by the root-level outputs.tf.
4. Ensure that each file is valid HCL and uses best practices for Terraform module structure.

You do NOT need to modify the root-level main.tf. You only generate the 3 module files: `main.tf`, `variables.tf`, and `outputs.tf` inside `output/final/terraform/modules/<module_name>/` for EACH module.

VARIABLE NAME PRESERVATION RULE: Look at each module block in main.tf and use the exact variable names that are passed to that module. For example, if a module uses `vpc_cidr`, `public_subnet_cidr`, `enable_flow_logs`, etc., then declare those exact same variable names in the module's variables.tf file.

Analyze the module names and their input variables to determine what AWS resources are appropriate for each module. Use the module name and variables to guide your implementation decisions.

Keep the implementation clean, modular, and production-ready.
""",
        expected_output=f"Three files under `output/final/terraform/modules/<module_name>/` for each of the {len(modules)} modules ({', '.join(modules)}): `main.tf`, `variables.tf`, and `outputs.tf` containing valid, complete, and functional Terraform module code.",
        agent=terraform_module_generator_agent,
        tools=[FileWriterTool()]
    )
       
    # Create the crew for module generation
    crew = Crew(
        agents=[terraform_module_generator_agent],
        tasks=[module_task],
        verbose=True,
        process=Process.sequential
    )
    
    # Run the crew to generate modules
    print("🚀 Running terraform module generator test with AI prompt...")
    result = crew.kickoff()
    
    print("\n✅ Terraform module generator test completed!")
    print(f"Result: {result}")
    
    # Check if modules were created
    created_modules = []
    missing_modules = set()
    
    if os.path.exists(modules_dir):
        print(f"✅ Modules directory created at {modules_dir}")
        
        # List created modules
        created_modules = [d for d in os.listdir(modules_dir) if os.path.isdir(os.path.join(modules_dir, d))]
        print(f"🔍 Found {len(created_modules)} created modules:")
        
        # Check for missing modules
        missing_modules = set(modules) - set(created_modules)
        if missing_modules:
            print(f"⚠️  WARNING: Missing modules: {', '.join(missing_modules)}")
            print("   This may be due to FileWriterTool errors during creation.")
        
        for module in created_modules:
            module_path = os.path.join(modules_dir, module)
            files = os.listdir(module_path)
            print(f"   - {module}: {files}")
            
            # Check for output blocks in main.tf
            main_tf_path = os.path.join(module_path, "main.tf")
            if os.path.exists(main_tf_path):
                with open(main_tf_path, "r") as f:
                    content = f.read()
                    if "output" in content:
                        print(f"   ❌ WARNING: {module}/main.tf contains output blocks!")

            expected_files = ['main.tf', 'variables.tf', 'outputs.tf']
            missing_files = [f for f in expected_files if f not in files]
            if missing_files:
                print(f"   ⚠️  WARNING: {module} missing files: {', '.join(missing_files)}")
    else:
        print("❌ Modules directory was not created!")
        # Set missing modules to all expected modules since none were created
        missing_modules = set(modules)
    
    # Summary
    print(f"\n📊 Summary:")
    print(f"   Expected modules: {len(modules)} ({', '.join(modules)})")
    print(f"   Created modules: {len(created_modules)} ({', '.join(created_modules)})")
    if missing_modules:
        print(f"   Missing modules: {len(missing_modules)} ({', '.join(missing_modules)})")
        print(f"   Recommendation: Re-run the script to generate missing modules.")
    
    # Run validation if modules were created
    validation_result = None
    if created_modules:
        print("\n🔍 Starting module validation...")
        
        # Create validation tasks for all created modules
        validation_tasks = create_validation_tasks(modules_dir, terraform_module_validator_agent)
        
        if validation_tasks:
            # Create validation crew
            validation_crew = Crew(
                agents=[terraform_module_validator_agent],
                tasks=validation_tasks,
                verbose=True,
                process=Process.sequential
            )
            
            # Run validation
            print("🚀 Running module validation...")
            validation_result = validation_crew.kickoff()
            
            print("\n✅ Module validation completed!")
            print(f"Validation Result: {validation_result}")
            
            # Save validation results to markdown file
            print("\n💾 Saving validation results...")
            saved_file = save_validation_results(validation_result, created_modules, modules_dir)
            if saved_file:
                print(f"📄 Validation report saved to: {saved_file}")
        else:
            print("⚠️  No validation tasks created - no modules to validate.")
    else:
        print("⚠️  Skipping validation - no modules were created successfully.")
    
    return validation_tasks

    
if __name__ == "__main__":
    module_generator() 