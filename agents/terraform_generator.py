# type: ignore
"""
Terraform Generator Agent Module.

This module defines the terraform generator agent that generates valid HCL Terraform code
organized by modules and resources.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.2)

terraform_generator_agent = Agent(
    name="TerraformGeneratorAgent",
    role="Terraform code generator",
    goal="Generate valid HCL Terraform code organized by modules and resources",
    backstory="Skilled in writing production-ready Terraform.",
    llm=llm,
    verbose=True
)
