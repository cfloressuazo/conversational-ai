import json

########################################
# Chat Properties
########################################
def craft_agent_chat_context(context: str) -> dict:
    """
    Craft the context for the agent to use for chat endpoints.
    """
    agent_chat_context = {
        "role": "system",
        "content": context
    }
    return agent_chat_context

def craft_agent_chat_first_message(content: str) -> dict:
    """
    Craft the first message for the agent to use for chat endpoints.
    """
    agent_chat_first_message = {
        "role": "assistant",
        "content": content
    }
    return agent_chat_first_message

def craft_agent_chat_instructions(instructions: str, response_shape: str) -> dict:
    """
    Craft the instructions for the agent to use for chat endpoints.
    """
    agent_instructions = {
        "role": "user",
        "content": instructions + f"\n\nFollow a RFC8259 compliant JSON with a shape of: {json.dumps(response_shape)} format without deviation."
    }
    return agent_instructions
