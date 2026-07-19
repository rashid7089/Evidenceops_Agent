from llama_index.core import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
# from llama_index.llms.openai import OpenAI
from llama_index.llms.openrouter import OpenRouter
from llama_index.llms.openai_like import OpenAILike

from app.config import config

import os
from dotenv import load_dotenv

load_dotenv()

# TODO: Complete Phase 1: add MODEL_PROVIDER option to support Ollama



def configure_models() -> None:
    # Configure the shared LLM and embedding model used by LlamaIndex.
    # Settings.llm = OpenAI(model=config.llm_model, temperature=0.1, api_key=config.chatgpt_api_key)
    # Settings.embed_model = OpenAIEmbedding(model=config.embedding_model)

    """
    Using OpenRouter because I struggled with OpenAI billing
    """
    Settings.llm = OpenRouter(
        api_key=config.openrouter_api_key,
        model=config.llm_model,
        temperature=0.1,  # Low temperature ensures deterministic, factual output
        is_function_calling_model=True,
    )
    # Settings.llm = OpenAILike(
    #     api_base="https://openrouter.ai/api/v1",
    #     api_key=config.openrouter_api_key,
    #     model=config.llm_model,
    #     temperature=0.1,
    #     # OpenRouter optional identification tracking parameters
    #     additional_kwargs={"headers": {"HTTP-Referer": "http://localhost:3000", "X-Title": "EvidenceOps"}}
    # )
    # Settings.llm = OpenAILike(
    #         api_base="https://openrouter.ai/api/v1",
    #         api_key=config.openrouter_api_key,
    #         model=config.llm_model,
    #         temperature=0.1,
    #         is_chat_model=True, # Tells the agent it can handle dialogue/tools
    #         additional_kwargs={"headers": {"HTTP-Referer": "http://localhost:3000", "X-Title": "EvidenceOps"}}
    #     )
    
            # Use OpenAILike and explicitly flag tool usage capabilities 
        # to satisfy the strict FunctionAgent validation requirements.
    Settings.llm = OpenAILike(
            api_base="https://openrouter.ai/api/v1",
            api_key=config.openrouter_api_key,
            model=config.llm_model,
            temperature=0.1,
            is_chat_model=True,
            is_function_calling_model=True,  # <--- ADD THIS CRITICAL LINE!
            # additional_kwargs={"headers": {"HTTP-Referer": "http://localhost:3000", "X-Title": "EvidenceOps"}}
        )
    
    Settings.embed_model = OpenAIEmbedding(
        api_base="https://openrouter.ai/api/v1",
        api_key=config.openrouter_api_key,
        model=config.embedding_model
    )