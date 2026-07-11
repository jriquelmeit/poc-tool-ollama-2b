from __future__ import annotations

from dataclasses import dataclass
from os import getenv

import requests
from dotenv import load_dotenv


class OllamaClientError(RuntimeError):
    pass


@dataclass(frozen=True)
class Settings:
    base_url: str
    model: str


def load_settings() -> Settings:
    load_dotenv()
    base_url = getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
    model = getenv("OLLAMA_MODEL", "gemma2:2b")
    return Settings(base_url=base_url, model=model)


def ask_ollama(settings: Settings, prompt: str) -> str:
    try:
        response = requests.post(
            f"{settings.base_url}/api/generate",
            json={
                "model": settings.model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaClientError(
            f"No se pudo conectar con Ollama en {settings.base_url}"
        ) from exc

    payload = response.json()
    return payload.get("response", "")
