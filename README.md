# 🤖 ollama-tool

`ollama-tool` es una CLI en Python para hablar con un servidor de Ollama desde terminal.
Está pensada como un POC simple para probar el modelo `gemma2:2b`, revisar código y validar un flujo local o remoto sin montar una interfaz web.

## ✨ ¿Qué hace?

- 🧠 Envía preguntas al modelo desde la terminal.
- 🔍 Revisa archivos, varios archivos o directorios completos.
- 🌐 Se conecta a un servidor Ollama remoto o local.
- ⚙️ Lee la configuración desde un archivo `.env`.
- 🚀 Permite probar rápidamente respuestas del modelo en consola.

## 🎯 Objetivo

El objetivo de este proyecto es tener una base mínima y funcional para:

1. Configurar una conexión a Ollama.
2. Ejecutar una CLI simple.
3. Probar `gemma2:2b` con preguntas reales.
4. Revisar código con uno o varios archivos o un directorio.
5. Escalar después a comandos como `summarize`, `explain` y `chat`.

## 🛠️ Tecnologías

- 🐍 Python 3.11+
- ⚡ `uv` para el entorno y dependencias
- 🧩 `Typer` para la CLI
- 🌍 `requests` para las llamadas HTTP
- 🔐 `python-dotenv` para leer `.env`
- 🎨 `rich` para salida más amigable en terminal

## 📁 Estructura

```text
poc-gemma2-2b/
  pyproject.toml
  .env
  .env.example
  README.md
  src/
    tool/
      __init__.py
      cli.py
      context.py
      commands/
        __init__.py
        review.py
      ollama_client.py
      prompts/
        review.md
```

## ✅ Requisitos

- Python 3.11 o superior
- `uv` instalado en tu sistema
- Un servidor Ollama accesible por red
- El modelo `gemma2:2b` disponible en ese servidor

## ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto con estas variables:

```env
OLLAMA_URL=http://MacBook-Pro-16-IA.local:11434
OLLAMA_MODEL=gemma2:2b
```

### Variables

- `OLLAMA_URL`: URL base del servidor Ollama.
- `OLLAMA_MODEL`: modelo que usará la CLI.

> Nota: `OLLAMA_URL` debe apuntar a la base del host, no al endpoint `/api/generate`.

## 📦 Instalación

### 1. Crear el entorno virtual

```bash
python3 -m uv venv .venv
```

### 2. Instalar dependencias

```bash
python3 -m uv add typer requests python-dotenv rich hatchling
```

### 3. Verificar la instalación

```bash
python3 -m uv run ollama-tool --help
```

## ▶️ Uso

### Hacer una pregunta

```bash
python3 -m uv run ollama-tool ask "hola"
```

### Otro ejemplo

```bash
python3 -m uv run ollama-tool ask "Explícame qué hace este fragmento de código"
```

### Revisar código

```bash
python3 -m uv run ollama-tool review src/main.py
python3 -m uv run ollama-tool review src/a.py src/b.py
python3 -m uv run ollama-tool review src/ --prompt "Busca bugs, riesgos y mejoras"
```

El comando `review` acepta archivos, varios archivos o directorios. Cuando recibe un directorio, recorre el contenido de forma recursiva e incluye archivos de texto relevantes.

El prompt por defecto de revisión vive en `src/tool/prompts/review.md`.

## 🔌 Conexión con Ollama

La CLI usa el endpoint:

- `POST /api/generate`

La URL final se construye a partir de `OLLAMA_URL`.

### Prueba manual

```bash
curl http://MacBook-Pro-16-IA.local:11434/api/tags
```

Si el servidor responde, la CLI debería poder comunicarse con Ollama sin problemas.

## 🧩 Comportamiento actual

- ✅ Carga configuración desde `.env`
- ✅ Usa `gemma2:2b` por defecto
- ✅ Ejecuta el comando `ask`
- ✅ Ejecuta el comando `review`
- ✅ Lee prompts por defecto desde archivos `.md`
- ✅ Muestra errores de conexión de forma clara

## 🛣️ Roadmap

- 📝 `summarize --diff`
- 🔍 `explain <archivo>`
- 💬 `chat` interactivo
- 📄 salida en JSON
- 🧭 mejor manejo de contexto de código

## 🧪 Troubleshooting

### No conecta con Ollama

Verifica que:

- Ollama esté corriendo en la máquina remota.
- El puerto `11434` esté abierto.
- `OLLAMA_URL` tenga la IP o host correctos.

Prueba rápida:

```bash
curl http://MacBook-Pro-16-IA.local:11434/api/tags
```

### El comando no aparece

Prueba:

```bash
python3 -m uv run ollama-tool --help
```

## 📌 Nota

Este proyecto está pensado para trabajar sin instalar dependencias globalmente.
Todo se ejecuta dentro del entorno virtual local usando `uv`.

## 🧠 Prompts

Los prompts por defecto se guardan en archivos Markdown dentro de `src/tool/prompts/`.
Esto facilita editar la instrucción de revisión sin tocar código.

## 📄 Licencia

Este proyecto está publicado bajo la licencia MIT. Revisa el archivo `LICENSE` para más detalles.
