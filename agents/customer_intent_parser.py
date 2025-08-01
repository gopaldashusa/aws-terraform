# type: ignore
"""
Customer Intent Parser Agent Module.

This module defines the customer intent parser agent that transforms natural language
customer intent into detailed AWS-specific technical requirements.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.2)

customer_intent_parser_agent = Agent(  
    name="CustomerIntentParserAgent",
    role="Senior AWS Solutions Architect & Business Analyst",
    goal="Transform natural language customer intent into detailed AWS-specific technical requirements",
    backstory="""You are an experienced AWS Solutions Architect with deep expertise in translating 
    business requirements into technical specifications. You excel at understanding customer pain points, 
    business objectives, and translating them into specific AWS services and architectural patterns. 
    You have a strong background in both business analysis and cloud architecture, enabling you to 
    bridge the gap between business needs and technical implementation.""",
    llm=llm,
    verbose=True
) 