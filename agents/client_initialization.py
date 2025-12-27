import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

load_dotenv()

class LLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
               raise ValueError("OPENAI_API_KEY not found when using OpenAI provider")
            self.client = OpenAI(api_key=api_key)
            self.mode = "openai"
            
        elif self.provider == "ollama":
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama3.2")
            self.client = ChatOllama(base_url=host, model=model)
            self.mode = "ollama"
            
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def create_response(self, **kwargs):
        if self.mode == "openai":
            return self.client.responses.create(**kwargs)
        elif self.mode == "ollama":
            # Convert OpenAI format to LangChain format
            messages = kwargs.get("messages", [])
            # Simple conversion - needs improvement
            prompt = "\n".join([msg.get("content", "") for msg in messages if msg.get("role") == "user"])
            response = self.client.invoke([HumanMessage(content=prompt)])
            # Wrap in OpenAI-like response
            class MockResponse:
                def __init__(self, content):
                    self.output_text = content
            return MockResponse(response.content)

# Global client instance
llm_client = LLMClient()
