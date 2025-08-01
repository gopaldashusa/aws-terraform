from crewai import Task
from prompts.task_prompts import PARSE_PROMPT, PLAN_DEPENDENCY_PROMPT, GENERATE_PROMPT, CUSTOMER_PARSE_PROMPT, DESIGN_PROMPT, CUSTOMER_INTENT_PARSE_PROMPT, DYNAMIC_VARIABLES_PROMPT, INFRA_PLAN_PROMPT
from agents.technical_req_parser import technical_req_parser_agent
from agents.terraform_planner import terraform_planner_agent
from agents.terraform_generator import terraform_generator_agent
from agents.customer_req_parser import customer_req_parser_agent
from agents.customer_intent_parser import customer_intent_parser_agent
#from agents.terraform_module_generator import terraform_module_generator_agent

def get_tasks(infra_request: str):
    return [
        Task(
            description=CUSTOMER_INTENT_PARSE_PROMPT.format(intent=infra_request),
            agent=customer_intent_parser_agent,
            expected_output="A comprehensive AWS infrastructure requirements document in markdown format.",
            output_file="output/customer_requirement.md"
        ),
        Task(
            description=CUSTOMER_PARSE_PROMPT.format(request=infra_request),
            agent=customer_req_parser_agent,
            expected_output="A comprehensive infrastructure planning document in markdown format.",
            output_file="output/final/planning_output.md"
        ),
        Task(
            description=DESIGN_PROMPT,
            agent=customer_req_parser_agent,
            expected_output="A detailed architecture design document in markdown format.",
            output_file="output/final/design_output.md"
        ),
        Task(
            description=INFRA_PLAN_PROMPT,
            agent=technical_req_parser_agent,
            expected_output="A well-structured JSON plan of AWS infra components.",
            output_file="output/infra_plan.json"
        ),
        Task(
            description=PLAN_DEPENDENCY_PROMPT,
            agent=terraform_planner_agent,
            expected_output="Planned dependency-aware infra in JSON format",
            output_file="output/infra_plan_with_dependencies.json"
        ),
        Task(
            description=DYNAMIC_VARIABLES_PROMPT,
            agent=terraform_generator_agent,
            expected_output="A comprehensive variables.tf file with dynamic parameters extracted from customer requirements.",
            output_file="output/final/terraform/variables.tf"
        ),
        Task(
            description=GENERATE_PROMPT,
            agent=terraform_generator_agent,
            expected_output="A main.tf file with Terraform code using dynamic variables defined.",
            output_file="output/final/terraform/main.tf"
        )
    ]
