from __future__ import annotations

import json
import re
from pathlib import Path


def _safe_session_name(session: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", session.strip())
    return cleaned or "default"


def session_path(session: str) -> Path:
    base_dir = Path.home() / ".config" / "ollama-tool" / "chat"
    return base_dir / f"{_safe_session_name(session)}.json"


def load_history(session: str) -> list[dict[str, str]]:
    path = session_path(session)
    if not path.exists():
        return []

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    if isinstance(payload, dict):
        messages = payload.get("messages", [])
    else:
        messages = payload

    if not isinstance(messages, list):
        return []

    history: list[dict[str, str]] = []
    for item in messages:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if isinstance(role, str) and isinstance(content, str):
            history.append({"role": role, "content": content})

    return history


def save_history(session: str, history: list[dict[str, str]]) -> None:
    path = session_path(session)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"messages": history}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_history(session: str) -> None:
    path = session_path(session)
    if path.exists():
        path.unlink()
