from __future__ import annotations

from llama_index.core import Settings 
from llama_index.core.agent.workflow import FunctionAgent
import inspect

# from llama_index.llms.openai import OpenAI
# from llama_index.llms.openrouter import OpenRouter


from app.config import config
from app.tools.research_tools import build_tools

MAX_TOOL_CALLS_PER_REQUEST = 1
SYSTEM_PROMPT = f"""
You are EvidenceOps, a careful research operations agent.
You have a maximam Limit of calling tools of {MAX_TOOL_CALLS_PER_REQUEST}

Operational rules:
1. Break complex requests into explicit subproblems.
2. Search the knowledge base before making factual claims.
3. Distinguish evidence, inference, and recommendation.
4. Never invent a citation or claim that a tool returned information it did not return.
5. Ask for human approval before saving a final report.
6. Record an audit event before and after a consequential action.
7. End with: findings, evidence limitations, confidence, and next action.
"""


def build_agent(approved_to_save = False) -> FunctionAgent:
    # print(inspect.signature(FunctionAgent.__init__))
    return FunctionAgent(
        name="EvidenceOpsAgent",
        description="Plans research, retrieves evidence, synthesizes findings, and prepares reports.",
        system_prompt=SYSTEM_PROMPT,
        tools=build_tools(approved_to_save=approved_to_save),
        llm=Settings.llm,
        max_iterations=MAX_TOOL_CALLS_PER_REQUEST
    )