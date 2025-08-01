# type: ignore
"""
Technical Requirement Parser Agent Module.

This module defines the technical requirement parser agent that converts infrastructure
planning and design documents into structured JSON.
"""

import os
from dotenv import load_dotenv
from crewai import Agent
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o"), temperature=0.3)

technical_req_parser_agent = Agent( 
    name="TechnicalReqParserAgent",
    role="Technical infrastructure requirement parser",
    goal="Convert infrastructure planning and design documents into structured JSON",
    backstory="Expert in parsing technical infrastructure documents and converting them into structured JSON plans.",
    llm=llm,
    verbose=True
)
