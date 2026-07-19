from __future__ import annotations

from pathlib import Path

import typer

from ..chat_store import clear_history, load_history, save_history
from ..ollama_client import OllamaClientError, chat_ollama_stream, load_settings
from ..output import console, render_markdown


def load_default_prompt() -> str:
    prompt_path = Path(__file__).resolve().parent.parent / "prompts" / "chat.md"
    return prompt_path.read_text(encoding="utf-8").strip()


def run_chat(reset: bool = False, session: str = "default") -> None:
    settings = load_settings()
    system_prompt = load_default_prompt()
    history: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    if reset:
        clear_history(session)
    else:
        saved_history = load_history(session)
        if saved_history:
            history.extend(saved_history)

    console.print("[bold cyan]Chat iniciado[/bold cyan]")
    console.print(f"[dim]Sesión: {session}[/dim]")
    console.print("Escribe `exit` o `quit` para salir, `reset` para limpiar el historial y `help` para ver comandos.")

    while True:
        try:
            user_input = console.input(f"[bold green]{settings.model}[/bold green]> ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print()
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            break

        if user_input.lower() == "help":
            console.print("[bold]Comandos internos:[/bold] `exit`, `quit`, `reset`, `help`")
            continue

        if user_input.lower() == "reset":
            history = [{"role": "system", "content": system_prompt}]
            clear_history(session)
            console.print("[yellow]Historial reiniciado[/yellow]")
            continue

        history.append({"role": "user", "content": user_input})

        try:
            console.print("[bold cyan]Cargando...[/bold cyan]")

            def print_chunk(chunk: str) -> None:
                console.print(chunk, end="")

            response = chat_ollama_stream(settings, history, on_chunk=print_chunk)
            console.print()
            history.append({"role": "assistant", "content": response})
            save_history(session, history[1:])
        except OllamaClientError as exc:
            typer.secho(str(exc), fg=typer.colors.RED, err=True)
