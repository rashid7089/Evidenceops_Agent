import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.base_dir = os.getcwd()
        self.storage_dir = self.validate_path("storage", False)
        self.__data_dir = self.validate_path("data")
        
        self.__chatgpt_api_key = ""
        self.chatgpt_api_base = "https://openrouter.ai"

        self.model_provider = os.getenv("MODEL_PROVIDER", "openai").lower()
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.embedding_model = os.getenv("self.", "text-embedding-3-small")

        self.top_k = 3

    def validate_path(self, folder_name, require_documents_inside = True):
        data_path = Path(self.base_dir+f"/{folder_name}")
        if not data_path.exists():
            raise RuntimeError(f"The folder {folder_name} doesn't exist on directory: '{data_path}'.")
        elif require_documents_inside and not any(data_path.iterdir()):
            raise RuntimeError(f"No documents found in the {folder_name} directory: '{data_path}'.")
        return data_path

    @property
    def chatgpt_api_key(self):
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY == None or OPENAI_API_KEY == "":
            raise Exception("Error: ChatGPT Key not found")
        return OPENAI_API_KEY

    @property
    def openrouter_api_key(self):
        OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
        if OPENROUTER_API_KEY == None or OPENROUTER_API_KEY == "":
            raise Exception("Error: OpenRouter Key not found")
        return OPENROUTER_API_KEY

    @property
    def data_dir(self):
        return self.__data_dir
    
    @data_dir.setter
    def data_dir(self, value):
        newPath = self.validate_path(value)
        self.__data_dir = newPath



load_dotenv()

config = Config()
