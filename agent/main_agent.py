from google.adk.agents import LlmAgent

# Constants
DEFAULT_MODEL = "gemini-1.5-pro"

# Agent configurations (easy to expand)
AGENT_CONFIGS = [
    {
        "name": "greeting_agent",
        "description": "Greet the lead politely.",
        "instruction": "Hey {lead_name}, thank you for filling out the form! I'd like to gather some information from you. Is that okay? (yes/no)"
    },
    {
        "name": "ask_age_agent",
        "description": "Ask the lead's age.",
        "instruction": "What is your age?"
    },
    {
        "name": "ask_country_agent",
        "description": "Ask the lead's country.",
        "instruction": "Which country are you from?"
    },
    {
        "name": "ask_interest_agent",
        "description": "Ask the lead's area of interest.",
        "instruction": "What product or service are you interested in?"
    },
    {
        "name": "thank_you_agent",
        "description": "Thank the lead.",
        "instruction": "Thank you for providing your information! Our team will contact you shortly."
    }
]

# Factory function to create agents
def create_llm_agent(name: str, description: str, instruction: str, model: str = DEFAULT_MODEL) -> LlmAgent:
    return LlmAgent(
        name=name,
        model=model,
        description=description,
        instruction=instruction
    )

# Create the sales pipeline using configurations
sales_agents_pipeline = [
    create_llm_agent(cfg["name"], cfg["description"], cfg["instruction"])
    for cfg in AGENT_CONFIGS
]
