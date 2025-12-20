from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_name: str = "llm-control-plane"
    environment: str = "local"
    log_dir: str = "logs"
    min_confidence_default: float = 0.3


settings = Settings()
