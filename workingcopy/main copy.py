from crewai import Crew
from tasks.tasks import get_tasks
from agents.terraform_generator import terraform_generator_agent
from agents.customer_req_parser import customer_req_parser_agent
from agents.technical_req_parser import technical_req_parser_agent
from agents.terraform_planner import terraform_planner_agent
from agents.customer_intent_parser import customer_intent_parser_agent
from agents.terraform_module_generator import terraform_module_generator_agent
from tools.prepostcheck import run_pre_checks, run_post_activities
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Run pre-execution checks and get customer intent
    customer_intent = run_pre_checks()
    if customer_intent is None:
        return

    # Create crew
    crew = Crew(
        agents=[
            customer_intent_parser_agent,
            customer_req_parser_agent,
            technical_req_parser_agent,
            terraform_planner_agent,
            terraform_generator_agent,
            terraform_module_generator_agent
        ],
        tasks=get_tasks(customer_intent),
        verbose=True
    )

    # Execute the crew
    result = crew.kickoff()

    # Run post-execution activities
    run_post_activities()

if __name__ == "__main__":
    main()
