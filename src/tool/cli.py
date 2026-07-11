from __future__ import annotations

import typer

from pathlib import Path

from .commands.review import run_review
from .ollama_client import OllamaClientError, ask_ollama, load_settings
from .output import console, render_markdown

app = typer.Typer(add_completion=False)


@app.callback()
def main():
    """Ollama CLI."""


@app.command()
def ask(question: str):
    """Ask Ollama a question."""
    settings = load_settings()
    prompt = f"Responde de forma breve y clara:\n\n{question}"
    try:
        with console.status("[bold cyan]Cargando...[/bold cyan]", spinner="dots"):
            response = ask_ollama(settings, prompt)
        render_markdown(response)
    except OllamaClientError as exc:
        typer.secho(str(exc), fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)


@app.command()
def review(
    paths: list[Path] = typer.Argument(..., exists=True, readable=True),
    prompt: str | None = typer.Option(None, "--prompt", help="Instrucción de revisión"),
):
    """Review files or directories with Ollama."""
    run_review(paths, prompt)


if __name__ == "__main__":
    app()
