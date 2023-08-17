from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import agents.api.schemas
import agents.crud
import agents.models
from agents.database import SessionLocal, engine
from agents.processing import (craft_agent_chat_context,
                               craft_agent_chat_first_message,
                               craft_agent_chat_instructions)
from agentsfwrk import integrations, logger

log = logger.get_logger(__name__)

agents.models.Base.metadata.create_all(bind = engine)

# Router basic information
router = APIRouter(
    prefix = "/agents",
    tags = ["Chat"],
    responses = {404: {"description": "Not found"}}
)

# Dependency: Used to get the database in our endpoints.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint for the router.
@router.get("/")
async def agents_root():
    return {"message": "Hello there conversational ai!"}

@router.get("/get-agents", response_model = List[agents.api.schemas.Agent])
async def get_agents(db: Session = Depends(get_db)):
    """
    Get all agents endpoint.
    """
    log.info("Getting all agents")
    db_agents = agents.crud.get_agents(db)
    log.info(f"Agents: {db_agents}")

    return db_agents

@router.post("/create-agent", response_model = agents.api.schemas.Agent)
async def create_agent(agent: agents.api.schemas.AgentCreate, db: Session = Depends(get_db)):
    """
    Create an agent endpoint.
    """
    log.info(f"Creating agent: {agent.json()}")
    db_agent = agents.crud.create_agent(db, agent)
    log.info(f"Agent created with id: {db_agent.id}")

    return db_agent

@router.get("/get-conversations", response_model = List[agents.api.schemas.Conversation])
async def get_conversations(agent_id: str, db: Session = Depends(get_db)):
    """
    Get all conversations for an agent endpoint.
    """
    log.info(f"Getting all conversations for agent id: {agent_id}")
    db_conversations = agents.crud.get_conversations(db, agent_id)
    log.info(f"Conversations: {db_conversations}")

    return db_conversations

@router.post("/create-conversation", response_model = agents.api.schemas.Conversation)
async def create_conversation(conversation: agents.api.schemas.ConversationCreate, db: Session = Depends(get_db)):
    """
    Create a conversation linked to an agent
    """
    log.info(f"Creating conversation assigned to agent id: {conversation.agent_id}")
    db_conversation = agents.crud.create_conversation(db, conversation)
    log.info(f"Conversation created with id: {db_conversation.id}")

    return db_conversation

@router.get("/get-messages", response_model = List[agents.api.schemas.Message])
async def get_messages(conversation_id: str, db: Session = Depends(get_db)):
    """
    Get all messages for a conversation endpoint.
    """
    log.info(f"Getting all messages for conversation id: {conversation_id}")
    db_messages = agents.crud.get_messages(db, conversation_id)
    log.info(f"Messages: {db_messages}")

    return db_messages

@router.post("/chat-agent", response_model = agents.api.schemas.ChatAgentResponse)
async def chat_completion(message: agents.api.schemas.UserMessage, db: Session = Depends(get_db)):
    """
    Get a response from the GPT model given a message from the client using the chat
    completion endpoint.

    The response is a json object with the following structure:
    ```
    {
        "conversation_id": "string",
        "response": "string"
    }
    ```
    """
    log.info(f"User conversation id: {message.conversation_id}")
    log.info(f"User message: {message.message}")

    conversation = agents.crud.get_conversation(db, message.conversation_id)

    if not conversation:
        # If there are no conversations, we can choose to create one on the fly OR raise an exception.
        # Which ever you choose, make sure to uncomment when necessary.

        # Option 1:
        # conversation = agents.crud.create_conversation(db, message.conversation_id)

        # Option 2:
        return HTTPException(
            status_code = 404,
            detail = "Conversation not found. Please create conversation first."
        )

    log.info(f"Conversation id: {conversation.id}")

    # NOTE: We are crafting the context first and passing the chat messages in a list
    # appending the first message (the approach from the agent) to it.
    context = craft_agent_chat_context(conversation.agent.context)
    chat_messages = [craft_agent_chat_first_message(conversation.agent.first_message)]

    # NOTE: Append to the conversation all messages until the last interaction from the agent
    # If there are no messages, then this has no effect.
    # Otherwise, we append each in order by timestamp (which makes logical sense).
    hist_messages = conversation.messages
    hist_messages.sort(key = lambda x: x.timestamp, reverse = False)
    if len(hist_messages) > 0:
        for mes in hist_messages:
            log.info(f"Conversation history message: {mes.user_message} | {mes.agent_message}")
            chat_messages.append(
                {
                    "role": "user",
                    "content": mes.user_message
                }
            )
            chat_messages.append(
                {
                    "role": "assistant",
                    "content": mes.agent_message
                }
            )
    # NOTE: We could control the conversation by simply adding
    # rules to the length of the history.
    # if len(hist_messages) > 10:
    #     # Finish the conversation gracefully.
    #     log.info("Conversation history is too long, finishing conversation.")
    #     api_response = agents.api.schemas.ChatAgentResponse(
    #         conversation_id = message.conversation_id,
    #         response        = "This conversation is over, good bye."
    #     )
    #     return api_response

    # Send the message to the AI agent and get the response
    service = integrations.OpenAIIntegrationService(
        context = context,
        instruction = craft_agent_chat_instructions(
            conversation.agent.instructions,
            conversation.agent.response_shape
        )
    )
    service.add_chat_history(messages = chat_messages)

    response = service.answer_to_prompt(
        # We can test different OpenAI models.
        model               = "gpt-3.5-turbo",
        prompt              = message.message,
        # We can test different parameters too.
        temperature         = 0.5,
        max_tokens          = 1000,
        frequency_penalty   = 0.5,
        presence_penalty    = 0
    )

    log.info(f"Agent response: {response}")

    # Prepare response to the user
    api_response = agents.api.schemas.ChatAgentResponse(
        conversation_id = message.conversation_id,
        response        = response.get('answer')
    )

    # Save interaction to database
    db_message = agents.crud.create_conversation_message(
        db = db,
        conversation_id = conversation.id,
        message = agents.api.schemas.MessageCreate(
            user_message = message.message,
            agent_message = response.get('answer'),
        ),
    )
    log.info(f"Conversation message id {db_message.id} saved to database")

    return api_response
