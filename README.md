# Simbie AI — Interview Exercise

## 1. Set your OpenAI API key

Copy the example env file and fill in your key:

```bash
cp .env.example .env
# then edit .env and set OPENAI_API_KEY=sk-...
```

Both run options below read `OPENAI_API_KEY` from this `.env` file. It is
gitignored and never baked into the Docker image.

## 2. Run

Pick one of the two options below.

### Option A — Python + venv

Requires Python 3.13 installed locally.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Load the key from .env into your shell, then run:
export $(grep -v '^#' .env | xargs)
python main.py
```

### Option B — Docker

Requires only Docker (no Python, no venv, no pip — the image bundles everything).
Compose loads `.env` automatically.

```bash
docker compose run --rm agent
```

Compose builds the image automatically on the first run. The project is mounted
into the container, so any later edits to the `.py` files are picked up
automatically — just re-run the command above, no rebuild needed.

(You only need to rebuild with `docker compose build` if you change
dependencies in `requirements.txt` since those are installed at build time., or any environment variables at `.env`)

## 3. Use

Select a clinic and talk to the agent.
Try giving it a date of birth like `1985-03-15`.
