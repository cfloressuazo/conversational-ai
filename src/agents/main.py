from fastapi import FastAPI

from agents.api.routes import router as ai_agents
from agentsfwrk.logger import setup_applevel_logger

log = setup_applevel_logger(file_name = 'agents.log')

app = FastAPI()
app.include_router(router = ai_agents)

@app.get("/")
async def root():
    return {"message": "Hello there conversational ai user!"}
