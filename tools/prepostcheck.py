import os
import subprocess
import shutil
import re
from typing import Dict, Tuple

def separate_terraform_files(input_file_path: str, output_dir: str) -> Dict[str, str]:
    """
    Separate a combined Terraform file into main.tf and outputs.tf
    
    Args:
        input_file_path: Path to the combined Terraform file
        output_dir: Directory to create the separated files
    
    Returns:
        Dictionary with file paths and their content
    """
    
    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file not found: {input_file_path}")
    
    # Read the combined file
    with open(input_file_path, 'r') as f:
        content = f.read()
    
    # Split content into main.tf and outputs.tf
    main_content, outputs_content = parse_terraform_content(content)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Write main.tf
    main_tf_path = os.path.join(output_dir, "main.tf")
    with open(main_tf_path, 'w') as f:
        f.write(main_content)
    
    # Write outputs.tf
    outputs_tf_path = os.path.join(output_dir, "outputs.tf")
    with open(outputs_tf_path, 'w') as f:
        f.write(outputs_content)
    
    return {
        "main.tf": main_content,
        "outputs.tf": outputs_content,
        "main_tf_path": main_tf_path,
        "outputs_tf_path": outputs_tf_path
    }

def parse_terraform_content(content: str) -> Tuple[str, str]:
    """
    Parse Terraform content and separate module blocks from output blocks
    Also removes any separator comments like '// outputs.tf'.
    
    Args:
        content: Raw Terraform file content
    
    Returns:
        Tuple of (main_content, outputs_content)
    """
    
    # Remove any markdown code blocks if present
    content = re.sub(r'```hcl\s*', '', content)
    content = re.sub(r'```\s*$', '', content)
    
    lines = content.split('\n')
    main_lines = []
    output_lines = []
    
    in_output_block = False
    in_module_block = False
    brace_count = 0
    
    for line in lines:
        stripped_line = line.strip()
        
        # Skip separator comments and empty lines
        if (stripped_line.lower().startswith('// outputs.tf') or 
            stripped_line.lower().startswith('// main.tf') or
            stripped_line == ''):
            continue
        
        # Handle "# outputs.tf" comment - move it to outputs
        if stripped_line == '# outputs.tf':
            output_lines.append(line)
            continue
        
        # Detect output blocks
        if stripped_line.startswith('output '):
            in_output_block = True
            output_lines.append(line)
            continue
        
        # Detect module blocks
        if stripped_line.startswith('module '):
            in_module_block = True
            main_lines.append(line)
            continue
        
        # Handle braces for block counting
        if '{' in line:
            brace_count += line.count('{')
        if '}' in line:
            brace_count -= line.count('}')
        
        # Add line to appropriate section
        if in_output_block:
            output_lines.append(line)
            if brace_count == 0 and in_output_block:
                in_output_block = False
        elif in_module_block:
            main_lines.append(line)
            if brace_count == 0 and in_module_block:
                in_module_block = False
        else:
            # Lines outside blocks go to main.tf (providers, variables, etc.)
            # But skip any output-related content
            if not stripped_line.startswith('output ') and not stripped_line.startswith('# Terraform outputs'):
                main_lines.append(line)
    
    # Remove any stray separator comments and duplicate headers from both outputs
    main_lines = [l for l in main_lines if not (
        l.strip().lower().startswith('// outputs.tf') or
        l.strip().lower().startswith('// main.tf') or
        l.strip() == '# Terraform outputs' or
        l.strip() == '```hcl' or
        l.strip() == '```'
    )]
    
    output_lines = [l for l in output_lines if not (
        l.strip().lower().startswith('// outputs.tf') or
        l.strip().lower().startswith('// main.tf') or
        l.strip() == '```hcl' or
        l.strip() == '```'
    )]
    
    # Clean up empty lines and format
    main_content = '\n'.join(main_lines).strip()
    outputs_content = '\n'.join(output_lines).strip()
    
    # Add markdown code blocks if content exists (without injected headers)
    if main_content:
        main_content = f"```hcl\n{main_content}\n```"
    
    if outputs_content:
        outputs_content = f"```hcl\n{outputs_content}\n```"
    
    return main_content, outputs_content

def check_input_file():
    """Check if the input file exists and read its content."""
    try:
        with open("input/customer_intent.md", "r") as file:
            customer_intent = file.read()
        print("✅ Input file found: input/customer_intent.md")
        return customer_intent
    except FileNotFoundError:
        print("❌ input/customer_intent.md not found!")
        print("Please create input/customer_intent.md with your infrastructure requirements.")
        return None

def cleanup_output_directories():
    """Clean up output directories by removing existing files and directories."""
    directories_to_clean = [
        "output",
        "output/final",
        "output/final/terraform",
        "output/final/terraform/modules"
    ]
    
    for directory in directories_to_clean:
        if os.path.exists(directory):
            try:
                if os.path.isdir(directory):
                    shutil.rmtree(directory)
                    print(f"🗑️  Cleaned directory: {directory}")
                else:
                    os.remove(directory)
                    print(f"🗑️  Removed file: {directory}")
            except Exception as e:
                print(f"⚠️  Warning: Could not clean {directory}: {e}")
    
    # Recreate the output directories
    os.makedirs("output", exist_ok=True)
    os.makedirs("output/final", exist_ok=True)
    os.makedirs("output/final/terraform", exist_ok=True)
    os.makedirs("output/final/terraform/modules", exist_ok=True)
    print("📁 Recreated output directories")

def generate_architecture_diagram():
    """Generate architecture diagram from design_output.md if it exists."""
    print("\n🔄 Generating architecture diagram...")
    try:
        # Check if design_output.md exists
        if os.path.exists("output/final/design_output.md"):
            # Run the mermaid converter
            result = subprocess.run([
                "python3", "tools/mermaid_converter.py", 
                "output/final/design_output.md", 
                "--output-dir", "output/final"
            ], capture_output=True, text=True, check=True)
            print("✅ Architecture diagram generated successfully!")
        else:
            print("⚠️  design_output.md not found. Skipping diagram generation.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating architecture diagram: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as e:
        print(f"❌ Unexpected error during diagram generation: {e}")

def separate_terraform_files_post():
    """Separate combined Terraform main.tf into main.tf and outputs.tf files."""
    print("\n🔄 Separating Terraform files...")
    try:
        # Check if main.tf exists
        if os.path.exists("output/final/terraform/main.tf"):
            # Run the terraform file separator
            result = separate_terraform_files(
                "output/final/terraform/main.tf", 
                "output/final/terraform/"
            )
            print("✅ Terraform files separated successfully!")
            print(f"   - main.tf: {result['main_tf_path']}")
            print(f"   - outputs.tf: {result['outputs_tf_path']}")
        else:
            print("⚠️  main.tf not found. Skipping Terraform file separation.")
    except Exception as e:
        print(f"❌ Error separating Terraform files: {e}")

def print_completion_summary():
    """Print a summary of generated files."""
    print("\n✅ All files generated successfully!")
    print("📁 Check the directories for:")
    print("   - output/customer_requirement.md (customer intent parser output)")
    print("   - output/final/planning_output.md (customer requirement parser output)")
    print("   - output/final/design_output.md (architecture design output)")
    print("   - output/final/architecture_diagram.png (visual architecture diagram)")
    print("   - output/infra_plan.json (technical requirement parser output)")
    print("   - output/infra_plan_with_dependencies.json (terraform planner output)")
    print("   - output/final/terraform/main.tf (terraform generator output)")
    print("   - output/final/terraform/outputs.tf (terraform outputs)")
    print("   - output/final/terraform/variables.tf (terraform variables)")

def run_pre_checks():
    """Run all pre-execution checks and cleanup."""
    print("🔍 Running pre-execution checks...")
    
    # Check input file
    customer_intent = check_input_file()
    if customer_intent is None:
        return None
    
    # Clean up output directories
    print("🧹 Cleaning up output directories...")
    cleanup_output_directories()
    
    return customer_intent

def run_post_activities():
    """Run all post-execution activities."""
    print("🎯 Running post-execution activities...")
    
    # Generate architecture diagram
    generate_architecture_diagram()
    
    # Separate Terraform files
    separate_terraform_files_post()
    
    # Print completion summary
    print_completion_summary() 