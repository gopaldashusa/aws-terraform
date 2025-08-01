#!/bin/bash

# Backup the project
echo "🔄 Backing up the project..."

zip -r aws-terraform-project-$(date +%Y%m%d_%H%M%S).zip . -x "crewenv/*" "*.pyc" "__pycache__/*" ".DS_Store" "*.log" "output-/*"
