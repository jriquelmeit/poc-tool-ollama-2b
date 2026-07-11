from __future__ import annotations

from pathlib import Path

import typer

from ..context import read_files_for_review
from ..ollama_client import OllamaClientError, ask_ollama, load_settings
from ..output import console, render_markdown


def load_default_prompt() -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "review.md"
    return prompt_path.read_text(encoding="utf-8").strip()


def run_review(paths: list[Path], prompt: str | None) -> None:
    settings = load_settings()
    review_prompt = prompt or load_default_prompt()
    code_context = read_files_for_review(paths)

    if not code_context:
        typer.secho("No se encontraron archivos de texto para revisar.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    final_prompt = f"Instrucción:\n{review_prompt}\n\n{code_context}"

    try:
        with console.status("[bold cyan]Cargando...[/bold cyan]", spinner="dots"):
            response = ask_ollama(settings, final_prompt)
        render_markdown(response)
    except OllamaClientError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
