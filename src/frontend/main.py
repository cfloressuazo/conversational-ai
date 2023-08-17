import streamlit as st
import requests

API_URL = "http://0.0.0.0:8000/agents"  # We will use our local URL and port defined of our microservice for this example

def get_agents():
    """
    Get the list of available agents from the API
    """
    response = requests.get(API_URL + "/get-agents")
    if response.status_code == 200:
        agents = response.json()
        return agents

    return []

def get_conversations(agent_id: str):
    """
    Get the list of conversations for the agent with the given ID
    """
    response = requests.get(API_URL + "/get-conversations", params = {"agent_id": agent_id})
    if response.status_code == 200:
        conversations = response.json()
        return conversations

    return []

def get_messages(conversation_id: str):
    """
    Get the list of messages for the conversation with the given ID
    """
    response = requests.get(API_URL + "/get-messages", params = {"conversation_id": conversation_id})
    if response.status_code == 200:
        messages = response.json()
        return messages

    return []

def send_message(agent_id, message):
    """
    Send a message to the agent with the given ID
    """
    payload = {"conversation_id": agent_id, "message": message}
    response = requests.post(API_URL + "/chat-agent", json = payload)
    if response.status_code == 200:
        return response.json()

    return {"response": "Error"}

def main():
    st.set_page_config(page_title = "🤗💬 AIChat")

    with st.sidebar:
        st.title("Conversational Agent Chat")

        # Dropdown to select agent
        agents = get_agents()
        agent_ids = [agent["id"] for agent in agents]
        selected_agent = st.selectbox("Select an Agent:", agent_ids)

        for agent in agents:
            if agent["id"] == selected_agent:
                selected_agent_context = agent["context"]
                selected_agent_first_message = agent["first_message"]

        # Dropdown to select conversation
        conversations = get_conversations(selected_agent)
        conversation_ids = [conversation["id"] for conversation in conversations]
        selected_conversation = st.selectbox("Select a Conversation:", conversation_ids)

        if selected_conversation is None:
            st.write("Please select a conversation from the dropdown.")
        else:
            st.write(f"**Selected Agent**: {selected_agent}")
            st.write(f"**Selected Conversation**: {selected_conversation}")

    # Display chat messages
    st.title("Chat")
    st.write("This is a chat interface for the selected agent and conversation. You can send messages to the agent and see its responses.")
    st.write(f"**Agent Context**: {selected_agent_context}")

    messages = get_messages(selected_conversation)
    with st.chat_message("assistant"):
        st.write(selected_agent_first_message)

    for message in messages:
        with st.chat_message("user"):
            st.write(message["user_message"])
        with st.chat_message("assistant"):
            st.write(message["agent_message"])

    # User-provided prompt
    if prompt := st.chat_input("Send a message:"):
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("Thinking..."):
            response = send_message(selected_conversation, prompt)
            with st.chat_message("assistant"):
                st.write(response["response"])

if __name__ == "__main__":
    main()
