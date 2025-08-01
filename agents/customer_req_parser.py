# type: ignore
"""
Customer Requirement Parser Agent Module.

This module defines the customer requirement parser agent that creates cost-optimized
infrastructure planning and design documents following FinOps best practices.
"""

import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.3)

customer_req_parser_agent = Agent( 
    name="CustomerReqParserAgent",
    role="Senior AWS Cloud Architect & FinOps Practitioner",
    goal="Parse customer requirements and create cost-optimized infrastructure planning and design documents following FinOps best practices",
    backstory="Expert AWS Cloud Architect with deep FinOps expertise. Specializes in designing cost-effective, scalable AWS infrastructures while applying FinOps principles including right-sizing, resource optimization, cost allocation, and budget management. Has successfully delivered hundreds of AWS projects staying within budget constraints.",
    llm=llm,
    verbose=True
) 