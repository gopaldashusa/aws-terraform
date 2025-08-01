#!/usr/bin/env python3
# type: ignore
"""
Terraform Module Generator Agent Module.

This module defines the terraform module generator agent that analyzes main.tf and generates complete Terraform modules with proper resources.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.2)

terraform_module_generator_agent = Agent(
    name="TerraformModuleGeneratorAgent",
    role="Terraform module generator",
    goal="Analyze main.tf, variables.tf, and outputs.tf to generate complete Terraform modules with proper resources",
    backstory="You are an expert in analyzing Terraform configurations and generating modular, production-ready AWS infrastructure code.",
    llm=llm,
    verbose=True
) 

terraform_module_validator_agent = Agent(
    name="TerraformModuleValidatorAgent",
    role="Terraform module validator",
    goal="Validate the generated Terraform modules to ensure they are correct and can be used in production",
    backstory="You are an expert in validating Terraform modules to ensure they are correct, and AWS resource blocks are using correct Terraform resource types and can be used in production.",
    llm=llm,
    verbose=True
) 
