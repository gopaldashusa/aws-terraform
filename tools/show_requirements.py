#!/usr/bin/env python3
"""
Simple script to display markdown files in a readable format
"""

import os
import sys

def show_markdown(file_path):
    """Display the markdown file in a readable format"""
    try:
        if not os.path.exists(file_path):
            print(f"❌ Error: Could not find {file_path}")
            print("Please ensure the file exists and the path is correct")
            return
        
        print(f"📁 Reading from: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract filename for display
        filename = os.path.basename(file_path)
        print(f"\n📋 {filename}")
        print("=" * 80)
        print()
        
        # Display the content with proper formatting
        for line in content.splitlines():
            print(line)
        
        print()
        print("=" * 80)
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        print("Please ensure the file exists and the path is correct")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) != 2:
        print("Usage: python3 show_requirements.py <markdown_file_path>")
        print("Example: python3 show_requirements.py input/customer_intent.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    show_markdown(file_path)

if __name__ == "__main__":
    main() 