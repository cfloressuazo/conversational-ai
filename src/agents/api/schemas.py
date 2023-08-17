from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


##########################################
# Internal schemas
##########################################
class ConversationBase(BaseModel):
    agent_id: str

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: str
    timestamp: datetime = datetime.utcnow()

    class Config:
        orm_mode = True

class AgentBase(BaseModel):
    context         : str
    first_message   : str
    response_shape  : str
    instructions    : str

class AgentCreate(AgentBase):
    pass

class Agent(AgentBase):
    id: str
    timestamp: datetime = datetime.utcnow()
    conversations: List[Conversation] = []

    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    user_message: str
    agent_message: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: str
    timestamp: datetime = datetime.utcnow()
    conversation_id: str

    class Config:
        orm_mode = True

##########################################
# API schemas
##########################################
class UserMessage(BaseModel):
    conversation_id: str
    message: str

class ChatAgentResponse(BaseModel):
    conversation_id: str
    response: str
