# -*- coding: utf-8 -*-
"""
✅ Summary of Capabilities You Now Have

Layer	Capability
ACP	Structured messages with metadata
A2A	Routing agents dynamically by name
MCP	Retry logic, status tracking, and failure escalation

"""

# Step 1: Message Builder Function
import uuid
import time

def build_acp_message(sender, receiver, intent, content, context=None, status="PENDING", retries=0):
    return {
        "id": str(uuid.uuid4()),
        "timestamp": time.time(),
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "content": content,
        "context": context or {},
        "status": status,      # PENDING, SUCCESS, FAILED
        "retries": retries,
    }

class A2ARouter:
    def __init__(self, agents, max_retries=2):
        self.agents = {agent.name: agent for agent in agents}
        self.max_retries = max_retries
        self.message_log = []

    def dispatch(self, message):
        self.message_log.append(message)
        agent_name = message["receiver"]

        if agent_name not in self.agents:
            print(f"❌ Unknown agent: {agent_name}")
            return build_acp_message(
                sender="Router",
                receiver=message["sender"],
                intent="error",
                content=f"Unknown agent: {agent_name}",
                status="FAILED",
                context={"original": message}
            )

        agent = self.agents[agent_name]

        try:
            response = agent.run(message)
            response["status"] = "SUCCESS"
            self.message_log.append(response)
            return response
        except Exception as e:
            message["retries"] += 1
            if message["retries"] <= self.max_retries:
                print(f"🔁 Retry {message['retries']} for {agent_name}")
                return self.dispatch(message)
            else:
                print(f"❌ Max retries reached for {agent_name}")
                return build_acp_message(
                    sender="Router",
                    receiver=message["sender"],
                    intent="failure_notification",
                    content=str(e),
                    status="FAILED",
                    context={"original": message}
                )

# Step 2: ACP Agent Wrapper
class ACPAgentWrapper:
    def __init__(self, agent, name, next_agent=None):
        self.agent = agent
        self.name = name
        self.next_agent = next_agent  # Optional routing

    def run(self, message):
        print(f"\n📨 {self.name} received message from {message['sender']} with intent '{message['intent']}'")

        input_text = message["content"]
        result = self.agent.execute(input_text)

        print(f"✅ {self.name} output: {result[:100]}...")

        return build_acp_message(
            sender=self.name,
            receiver=self.next_agent or "Final",
            intent="processed_result",
            content=result,
            context={"prev_message": message}
        )


# Step 3: Orchestrator - Running Agents Sequentially (ACP Flow)
if __name__ == "__main__":
    # Replace with real CrewAI agents
    agents = [
        ACPAgentWrapper(MockAgent("CustomerIntentParser"), "CustomerIntentParser", next_agent="CustomerReqParser"),
        ACPAgentWrapper(MockAgent("CustomerReqParser"), "CustomerReqParser", next_agent="TechnicalReqParser"),
        ACPAgentWrapper(MockAgent("TechnicalReqParser"), "TechnicalReqParser", next_agent="TerraformPlanner"),
        ACPAgentWrapper(MockAgent("TerraformPlanner"), "TerraformPlanner", next_agent="TerraformGenerator"),
        ACPAgentWrapper(MockAgent("TerraformGenerator"), "TerraformGenerator", next_agent="TerraformModuleGenerator"),
        ACPAgentWrapper(MockAgent("TerraformModuleGenerator"), "TerraformModuleGenerator", next_agent="Final"),
    ]

    router = A2ARouter(agents)

    # Initial user message
    customer_intent = "Create a VPC with public/private subnets and RDS using Terraform"
    initial_message = build_acp_message(
        sender="User",
        receiver="CustomerIntentParser",
        intent="parse_customer_intent",
        content=customer_intent
    )

    # Dispatch initial message
    current_message = initial_message
    while current_message["receiver"] != "Final":
        current_message = router.dispatch(current_message)

    print("\n📜 Final Message Log:")
    for msg in router.message_log:
        print(f"[{msg['sender']} ➝ {msg['receiver']}] {msg['intent']} ({msg['status']})")

"""
Want Next?

- Add parallel dispatch (fork tasks to multiple agents)
- Use intent to choose receivers dynamically (e.g. use a RouterAgent to parse intent)
- Visualize message logs as sequence diagrams

""" 
