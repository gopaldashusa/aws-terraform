#!/bin/bash

# AWS Terraform Infrastructure Automation - Environment Setup Script

echo "🔧 Setting up virtual environment for AWS Terraform project..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
python3.11 -m venv crewenv
fi


# Activate virtual environment
echo "🔄 Activating virtual environment..."
source crewenv/bin/activate

# run the demo script
echo ""

echo "🚀 Running the demo for infrastructure generation"
echo "python awsdemo.py"
python awsdemo.py

#echo "🚀 Running the demo for terraform modules generation"
#echo "python awsdemo_modules.py"
#python awsdemo_modules.py  # To generate terraform modules
