from __future__ import annotations

from dataclasses import dataclass
import json
from os import getenv
from typing import Any, Callable

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


def chat_ollama(settings: Settings, messages: list[dict[str, str]]) -> str:
    return chat_ollama_stream(settings, messages, on_chunk=None)


def chat_ollama_stream(
    settings: Settings,
    messages: list[dict[str, str]],
    on_chunk: Callable[[str], None] | None,
) -> str:
    try:
        response = requests.post(
            f"{settings.base_url}/api/chat",
            json={
                "model": settings.model,
                "messages": messages,
                "stream": True,
            },
            stream=True,
            timeout=120,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise OllamaClientError(
            f"No se pudo conectar con Ollama en {settings.base_url}"
        ) from exc

    parts: list[str] = []
    try:
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            payload: dict[str, Any] = json.loads(line)
            message = payload.get("message", {})
            content = message.get("content", "")
            if content:
                parts.append(content)
                if on_chunk is not None:
                    on_chunk(content)
    finally:
        response.close()

    return "".join(parts)
