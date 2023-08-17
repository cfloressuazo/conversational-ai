import uuid
from sqlalchemy.orm import Session
from agents import models
from agents.api import schemas

def get_agents(db: Session):
    """
    Get all agents
    """
    return db.query(models.Agent).all()

def get_agent(db: Session, agent_id: str):
    """
    Get an agent by its id
    """
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def create_agent(db: Session, agent: schemas.AgentCreate):
    """
    Create an agent in the database
    """
    db_agent = models.Agent(
        id              = str(uuid.uuid4()),
        context         = agent.context,
        first_message   = agent.first_message,
        response_shape  = agent.response_shape,
        instructions    = agent.instructions
    )
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)

    return db_agent

def get_conversation(db: Session, conversation_id: str):
    """
    Get a conversation by its id
    """
    return db.query(models.Conversation).filter(models.Conversation.id == conversation_id).first()

def get_conversations(db: Session, agent_id: str):
    """
    Get all conversations for an agent
    """
    return db.query(models.Conversation).filter(models.Conversation.agent_id == agent_id).all()

def create_conversation(db: Session, conversation: schemas.ConversationCreate):
    """
    Create a conversation
    """
    db_conversation = models.Conversation(
        id          = str(uuid.uuid4()),
        agent_id    = conversation.agent_id,
    )
    db.add(db_conversation)
    db.commit()
    db.refresh(db_conversation)

    return db_conversation

def get_messages(db: Session, conversation_id: str):
    """
    Get all messages for a conversation
    """
    return db.query(models.Message).filter(models.Message.conversation_id == conversation_id).all()

def create_conversation_message(db: Session, message: schemas.MessageCreate, conversation_id: str):
    """
    Create a message for a conversation
    """
    db_message = models.Message(
        id              = str(uuid.uuid4()),
        user_message    = message.user_message,
        agent_message   = message.agent_message,
        conversation_id = conversation_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
