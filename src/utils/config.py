"""
Application configuration using Pydantic Settings
"""
from pathlib import Path
from typing import Optional, Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Project Settings
    project_name: str = Field(default="agentic-ai-app", description="Project name")
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: str = "INFO"
    
    # LLM Provider
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    anthropic_api_key: Optional[str] = None
    anthropic_model: str = "claude-3-5-sonnet-20241022"
    
    # GCP
    google_application_credentials: Optional[Path] = None
    gcp_project_id: Optional[str] = None
    gcp_region: str = "us-central1"
    vertex_ai_model: str = "gemini-pro"
    
    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: Optional[str] = None
    langchain_project: Optional[str] = None
    
    # Vector Database
    pinecone_api_key: Optional[str] = None
    pinecone_environment: Optional[str] = None
    pinecone_index_name: str = "default-index"
    
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    chroma_collection_name: str = "default-collection"
    
    # Application
    app_host: str = "0.0.0.0"
    app_port: int = 8080
    app_workers: int = 4
    
    # Security
    secret_key: str = Field(default="change-me-in-production", description="Secret key for sessions")
    
    @property
    def base_dir(self) -> Path:
        """Get project base directory"""
        return Path(__file__).parent.parent.parent
    
    @property
    def data_dir(self) -> Path:
        """Get data directory"""
        return self.base_dir / "data"
    
    @property
    def logs_dir(self) -> Path:
        """Get logs directory"""
        logs = self.base_dir / "logs"
        logs.mkdir(exist_ok=True)
        return logs


# Global settings instance
settings = Settings()
