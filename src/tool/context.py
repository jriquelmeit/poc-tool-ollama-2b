from __future__ import annotations

from pathlib import Path


DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "node_modules",
    "__pycache__",
}

TEXT_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".toml",
    ".json",
    ".yml",
    ".yaml",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".csv",
    ".ini",
    ".cfg",
    ".env",
}


def is_text_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(1024)
        return b"\x00" not in chunk
    except OSError:
        return False


def collect_text_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_file():
            if is_text_file(path):
                files.append(path)
            continue

        if path.is_dir():
            for candidate in path.rglob("*"):
                if any(part in DEFAULT_EXCLUDED_DIRS for part in candidate.parts):
                    continue
                if candidate.is_file() and is_text_file(candidate):
                    files.append(candidate)

    return files


def read_files_for_review(paths: list[Path], max_bytes_per_file: int = 20000) -> str:
    sections: list[str] = []
    for file_path in collect_text_files(paths):
        try:
            content = file_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        if len(content.encode("utf-8")) > max_bytes_per_file:
            content = content[:max_bytes_per_file] + "\n... [truncated]"

        sections.append(f"Archivo: {file_path.as_posix()}\n{content}")

    return "\n\n".join(sections)
