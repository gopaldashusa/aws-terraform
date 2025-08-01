#!/usr/bin/env python3
"""
Mermaid Diagram Converter Utility

This utility extracts Mermaid diagrams from markdown files and converts them to PNG images
for better visualization. It uses the mermaid-cli (mmdc) tool for conversion.
"""

import re
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import json


class MermaidConverter:
    """Utility class for converting Mermaid diagrams to PNG images."""
    
    def __init__(self, output_dir: str = "output/diagrams"):
        """
        Initialize the Mermaid converter.
        
        Args:
            output_dir: Directory to save generated PNG files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def check_mermaid_cli(self) -> bool:
        """
        Check if mermaid-cli is installed.
        
        Returns:
            True if mermaid-cli is available, False otherwise
        """
        try:
            result = subprocess.run(
                ["mmdc", "--version"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            print(f"✅ Mermaid CLI found: {result.stdout.strip()}")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Mermaid CLI (mmdc) not found.")
            print("Please install it using: npm install -g @mermaid-js/mermaid-cli")
            return False
    
    def extract_mermaid_diagrams(self, markdown_file: str) -> List[Tuple[str, str]]:
        """
        Extract Mermaid diagrams from a markdown file.
        
        Args:
            markdown_file: Path to the markdown file
            
        Returns:
            List of tuples containing (diagram_name, mermaid_code)
        """
        diagrams = []
        
        try:
            with open(markdown_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"❌ File not found: {markdown_file}")
            return diagrams
        except Exception as e:
            print(f"❌ Error reading file {markdown_file}: {e}")
            return diagrams
        
        # Pattern to match Mermaid code blocks
        pattern = r'```mermaid\s*\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        if not matches:
            print(f"📄 No Mermaid diagrams found in {markdown_file}")
            return diagrams
        
        print(f"🔍 Found {len(matches)} Mermaid diagram(s) in {markdown_file}")
        
        for i, mermaid_code in enumerate(matches):
            # Generate a name for the diagram
            diagram_name = f"diagram_{i+1}"
            
            # Try to extract a more meaningful name from the diagram content
            if "graph" in mermaid_code.lower():
                diagram_name = "architecture_diagram"
            elif "flowchart" in mermaid_code.lower():
                diagram_name = "flowchart"
            elif "sequence" in mermaid_code.lower():
                diagram_name = "sequence_diagram"
            elif "class" in mermaid_code.lower():
                diagram_name = "class_diagram"
            elif "er" in mermaid_code.lower():
                diagram_name = "entity_relationship"
            
            diagrams.append((diagram_name, mermaid_code.strip()))
        
        return diagrams
    
    def convert_to_png(self, mermaid_code: str, output_filename: str) -> bool:
        """
        Convert Mermaid code to PNG using mermaid-cli.
        
        Args:
            mermaid_code: The Mermaid diagram code
            output_filename: Name for the output PNG file
            
        Returns:
            True if conversion successful, False otherwise
        """
        output_path = self.output_dir / f"{output_filename}.png"
        
        try:
            # Create a temporary input file
            input_file = self.output_dir / f"{output_filename}.mmd"
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            
            # Run mermaid-cli conversion
            cmd = [
                "mmdc",
                "-i", str(input_file),
                "-o", str(output_path),
                "-t", "neutral",
                "-C", "tools/white_background.css",
                "-b", "white",
                "-s", "3.2"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Clean up temporary input file
            input_file.unlink(missing_ok=True)
            
            print(f"✅ Successfully converted to: {output_path}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Conversion failed: {e}")
            print(f"Error output: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error during conversion: {e}")
            return False
    
    def process_markdown_file(self, markdown_file: str) -> List[str]:
        """
        Process a markdown file and convert all Mermaid diagrams to PNG.
        
        Args:
            markdown_file: Path to the markdown file
            
        Returns:
            List of generated PNG file paths
        """
        if not self.check_mermaid_cli():
            return []
        
        diagrams = self.extract_mermaid_diagrams(markdown_file)
        generated_files = []
        
        for diagram_name, mermaid_code in diagrams:
            print(f"\n🔄 Converting {diagram_name}...")
            if self.convert_to_png(mermaid_code, diagram_name):
                generated_files.append(str(self.output_dir / f"{diagram_name}.png"))
        
        return generated_files
    
    def process_directory(self, directory_path: str, pattern: str = "*design_output_raw.md") -> dict:
        """
        Process all markdown files in a directory that match the pattern.
        
        Args:
            directory_path: Directory to search for markdown files
            pattern: Glob pattern to match files
            
        Returns:
            Dictionary mapping input files to generated PNG files
        """
        if not self.check_mermaid_cli():
            return {}
        
        directory = Path(directory_path)
        if not directory.exists():
            print(f"❌ Directory not found: {directory_path}")
            return {}
        
        results = {}
        
        for markdown_file in directory.rglob(pattern):
            print(f"\n📁 Processing: {markdown_file}")
            generated_files = self.process_markdown_file(str(markdown_file))
            if generated_files:
                results[str(markdown_file)] = generated_files
        
        return results


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert Mermaid diagrams to PNG images")
    parser.add_argument("input", help="Input markdown file or directory")
    parser.add_argument("--output-dir", default="output/diagrams", help="Output directory for PNG files")
    parser.add_argument("--pattern", default="*design_output_raw.md", help="File pattern for directory processing")
    
    args = parser.parse_args()
    
    converter = MermaidConverter(args.output_dir)
    
    input_path = Path(args.input)
    
    if input_path.is_file():
        print(f"🎯 Processing single file: {input_path}")
        generated_files = converter.process_markdown_file(str(input_path))
        if generated_files:
            print(f"\n📊 Generated {len(generated_files)} PNG file(s):")
            for file_path in generated_files:
                print(f"  - {file_path}")
        else:
            print("❌ No diagrams were converted.")
    
    elif input_path.is_dir():
        print(f"🎯 Processing directory: {input_path}")
        results = converter.process_directory(str(input_path), args.pattern)
        
        if results:
            print(f"\n📊 Summary:")
            total_files = sum(len(files) for files in results.values())
            print(f"  - Processed {len(results)} input file(s)")
            print(f"  - Generated {total_files} PNG file(s)")
            
            for input_file, generated_files in results.items():
                print(f"\n  📄 {input_file}:")
                for file_path in generated_files:
                    print(f"    - {file_path}")
        else:
            print("❌ No diagrams were converted.")
    
    else:
        print(f"❌ Input path does not exist: {input_path}")
        sys.exit(1)


if __name__ == "__main__":
    main() 