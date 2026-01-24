# Greek Verb Conjugation API

A local REST API that translates English verbs to Modern Greek and generates present-tense conjugations using an AI-as-a-Judge architecture powered by LangChain and Ollama.

## How It Works

- **Generator LLM**: Receives an English verb, translates it to Greek, and generates 6 present-tense conjugations with pronouns
- **Judge LLM**: Validates the generator's output, corrects any errors, assigns a confidence score, and provides notes
- **Final Output**: Only the judge-validated result is returned to the user, ensuring accuracy

## Setup

1. **Install Ollama and pull the model:**
   ```bash
   ollama pull llama3.1:8b
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask app:**
   ```bash
   export FLASK_APP=app.app:create_app
   flask run
   ```

## Usage

**Example request:**
```bash
curl -X POST http://localhost:5000/conjugate \
  -H "Content-Type: application/json" \
  -d '{"verb": "to write"}'
```

**Example response:**
```json
{
  "english": "to write",
  "greek": "γράφω",
  "conjugations": [
    { "pronoun": "εγώ", "form": "γράφω" },
    { "pronoun": "εσύ", "form": "γράφεις" },
    { "pronoun": "αυτός/αυτή/αυτό", "form": "γράφει" },
    { "pronoun": "εμείς", "form": "γράφουμε" },
    { "pronoun": "εσείς", "form": "γράφετε" },
    { "pronoun": "αυτοί/αυτές/αυτά", "form": "γράφουν" }
  ],
  "confidence": 0.95,
  "notes": "All conjugations are correct."
}
```

## Testing

The project includes a comprehensive test suite covering API endpoints and chain logic.

**Run all tests:**
```bash
pytest
```

**Run fast tests only (skip LLM calls):**
```bash
pytest -m "not slow"
```

**Run with verbose output:**
```bash
pytest -v
```

**Test coverage:**
- API endpoint validation (health, conjugate)
- Request/response structure validation
- Chain creation and JSON output
- Full integration tests with actual LLM calls
