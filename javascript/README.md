# Simbie AI — Interview Exercise (JavaScript / Node)

JavaScript port of the scheduling agent. Runs directly with Node — no build step.

## 1. Set your OpenAI API key

Copy the example env file from the repo root and fill in your key:

```bash
cp ../.env.example .env
# then edit .env and set OPENAI_API_KEY=sk-...
```

## 2. Install & run

Requires Node.js 18+ (uses native `fetch` and `readline/promises`).

```bash
npm install

# Load the key from .env into your shell, then run:
export $(grep -v '^#' .env | xargs)
npm start
```

Or in one line without a `.env` file:

```bash
OPENAI_API_KEY=sk-... npm start
```

## 3. Use

Talk to the agent. Try giving it a date of birth like `1985-03-15`.

## Files

- `main.js` — entry point
- `agent.js` — agent loop + tool scaffolding (fill in `TOOL_DEFINITIONS` / `TOOL_FUNCTIONS`)
- `ehr_services/mock_data.js` — mock EHR data (read to understand the format; do not modify)
