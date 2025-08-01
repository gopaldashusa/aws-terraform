# type: ignore
"""
Terraform Planner Agent Module.

This module defines the terraform planner agent that plans resource dependencies
and modules for AWS infrastructure.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.3)

terraform_planner_agent = Agent(
    name="TerraformPlannerAgent",
    role="Terraform dependency planner",
    goal="Plan resource dependencies and modules and align to the WAF ** AWS Well-Architected Framework **",
    backstory="Expert in AWS Terraform architecture who can plan a dependency-aware, WAF-aligned JSON with proper resource dependencies and modules",
    llm=llm,
    verbose=True
)
