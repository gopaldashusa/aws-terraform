# -*- coding: utf-8 -*-
"""
Agent Communication Protocol (ACP) Style Implementation
This file demonstrates how to implement ACP-style agent communication
using structured messages instead of raw strings.
"""

# Step 1: Message Builder Function
def build_acp_message(sender, receiver, intent, content, context=None):
    """
    Build a structured ACP message.
    
    Args:
        sender: Name of the sending agent
        receiver: Name of the receiving agent
        intent: Purpose of the message
        content: Actual message content
        context: Optional context dictionary
    
    Returns:
        dict: Structured message
    """
    return {
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "content": content,
        "context": context or {},
    }


# Step 2: ACP Agent Wrapper
class ACPAgentWrapper:
    """
    Wrapper class that adapts any agent to use ACP-style messaging.
    """
    
    def __init__(self, agent, name):
        """
        Initialize the wrapper.
        
        Args:
            agent: The actual agent (e.g., from CrewAI)
            name: Logical name for message routing
        """
        self.agent = agent
        self.name = name

    def run(self, message):
        """
        Process a message using the wrapped agent.
        
        Args:
            message: ACP-style message dictionary
            
        Returns:
            dict: Response message in ACP format
        """
        print(f"\n🔄 {self.name} received message from {message['sender']} (Intent: {message['intent']})")

        input_text = message["content"]

        # Agent should implement .execute(input_text) or similar
        result = self.agent.execute(input_text)

        print(f"✅ {self.name} produced output: {result[:120]}...")  # Truncated

        return build_acp_message(
            sender=self.name,
            receiver="next",  # Will be replaced by orchestrator
            intent="processed_result",
            content=result,
            context={"previous": message}
        )


# Mock Agent for demonstration
class MockAgent:
    """
    Mock agent for testing the ACP implementation.
    """
    
    def __init__(self, suffix):
        """
        Initialize mock agent.
        
        Args:
            suffix: Suffix to append to responses
        """
        self.suffix = suffix

    def execute(self, text):
        """
        Mock execution method.
        
        Args:
            text: Input text
            
        Returns:
            str: Mock response
        """
        return f"[{self.suffix}]: {text}"


# Step 3: Orchestrator - Running Agents Sequentially (ACP Flow)
def run_acp_pipeline(agents, customer_intent):
    """
    Run a pipeline of agents using ACP-style messaging.
    
    Args:
        agents: List of ACPAgentWrapper instances
        customer_intent: Initial customer intent
        
    Returns:
        list: Message log showing the flow
    """
    # Initial message from user
    message = build_acp_message(
        sender="User",
        receiver=agents[0].name,
        intent="parse_customer_intent",
        content=customer_intent
    )

    message_log = [message]

    for i, agent in enumerate(agents):
        # Set receiver for current message
        if i + 1 < len(agents):
            message["receiver"] = agents[i + 1].name
        else:
            message["receiver"] = "Final"

        message = agent.run(message)
        message_log.append(message)

    return message_log


# Step 4: Main execution
if __name__ == "__main__":
    # Replace MockAgent with your real CrewAI agents
    acp_agents = [
        ACPAgentWrapper(MockAgent("CustomerIntentParser"), "CustomerIntentParser"),
        ACPAgentWrapper(MockAgent("CustomerReqParser"), "CustomerReqParser"),
        ACPAgentWrapper(MockAgent("TechnicalReqParser"), "TechnicalReqParser"),
        ACPAgentWrapper(MockAgent("TerraformPlanner"), "TerraformPlanner"),
        ACPAgentWrapper(MockAgent("TerraformGenerator"), "TerraformGenerator"),
        ACPAgentWrapper(MockAgent("TerraformModuleGenerator"), "TerraformModuleGenerator"),
    ]

    # Simulated input from user
    customer_intent = "Create a secure 3-tier VPC on AWS with EC2, RDS, and S3, following best practices."

    logs = run_acp_pipeline(acp_agents, customer_intent)

    print("\n📜 Final Message Log:")
    for msg in logs:
        print(f"{msg['sender']} ➝ {msg['receiver']} ({msg['intent']})")


"""
Additional Features You Could Add:

- Timeout handling
- Failure retries  
- Contextual escalation
- Agent fallback

This approach:

- Decouples your agents from raw strings — they now communicate via structured messages.
- Mimics Agent Communication Protocol like in AutoGen or FIPA-style systems.
- Is easily extensible with routing agents, blackboards, or LangGraph migration later.

What You Can Do Next:

✅ Replace MockAgent with actual CrewAI agent instances (.execute() method)
🧠 Extend message structure to include timestamp, status, or reasoning
🚨 Add error handling, retries, or even parallel agent branches
🔄 Use message_log to create audit trail or rollback history

MCP (Message Control Protocol) Layer:
This manages:

- Retry on failure
- Timeout or agent failure handling
- Acknowledgment (ACK) or failure messages
- Optional delivery guarantees

A2A (Agent-to-Agent) Layer:
This is your message router / coordinator. Instead of hardcoding the flow (like a Python for loop), 
agents can send messages to any other agent dynamically based on logic.

Think of A2A as enabling:

- Peer-to-peer or non-linear routing (not just sequential)
- Agent addressing by name
- Dispatching based on intent or content


""" 