# SPEC: Greek Verb Conjugation API (AI-as-a-Judge)

## Objective
Create a local, free, Python REST API that:
- Accepts an English verb
- Translates it to Modern Greek
- Generates 6 present-tense conjugations with pronouns
- Uses a second LLM as a judge to validate and correct results
- Returns only judge-validated output

## Hard Constraints (Do Not Deviate)
- Python 3.10+
- Flask (NOT FastAPI)
- LangChain for LLM orchestration
- Ollama for local LLM execution
- No paid APIs
- No frontend
- No async
- No databases
- JSON-only inputs and outputs

## Model Requirements
- Use ChatOllama
- Generator model: llama3.1:8b
- Judge model: qwen2.5:14b (larger model for better validation)
- temperature=0
- format="json" (enforce JSON output)
- Generator and Judge MUST be separate chains

## Architecture
POST /conjugate
  → Generator LLM (translate + conjugate)
  → Judge LLM (validate + correct + score)
  → Return validated JSON

The generator output is NEVER returned directly.

## Project Structure
simple-translation/
├── app/
│   ├── __init__.py
│   ├── app.py          # Flask routes and app factory
│   ├── chains.py       # LangChain generator and judge chains
│   ├── prompts.py      # LLM prompt templates with few-shot examples
│   └── schemas.py      # Data models and schemas
├── tests/
│   ├── __init__.py
│   ├── test_api.py     # API endpoint tests
│   └── test_chains.py  # Chain logic tests
├── venv/               # Virtual environment (not in git)
├── .gitignore          # Git exclusions
├── pytest.ini          # Test configuration
├── requirements.txt    # Python dependencies
├── README.md           # Documentation
└── spec.md             # This specification

## Dependencies (requirements.txt)
- flask==3.0.0
- langchain==0.1.0
- langchain-community==0.0.10
- pytest==7.4.3 (testing)
- pytest-timeout==2.2.0 (testing)

## API Contract

### Endpoint
POST /conjugate

### Request Body
{
  "verb": "to write"
}

### Success Response (Shape Must Match)
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

## Error Handling
- 400 → invalid JSON or missing verb
- 500 → malformed LLM output or judge failure

## Prompt Requirements

### Generator Prompt MUST:
- Translate English → Modern Greek
- Generate EXACTLY 6 present-tense conjugations
- Include pronouns
- Return JSON ONLY
- No explanation text
- **Include few-shot examples** (2+ examples for better accuracy)

### Judge Prompt MUST:
- Validate correctness of conjugations
- Correct any errors
- Assign confidence score (0.0–1.0)
- Include brief notes
- Return JSON ONLY
- Be treated as the final authority
- **Include reference examples** of correct conjugations

## LangChain Implementation Rules
- Use PromptTemplate
- Use ChatOllama with `format="json"` for structured output
- Use | runnable composition
- Generator and Judge must be distinct chains
- Do NOT combine generation and judging into one prompt
- Do NOT introduce LangSmith, tools, or agents
- Parse and validate JSON output from both chains

## Flask App Rules
- Use app factory pattern
- Synchronous routes only
- JSON in / JSON out
- No auth
- No middleware beyond basics

## Local Execution Requirements

### Setup
```bash
# Pull required models
ollama pull llama3.1:8b    # Generator model
ollama pull qwen2.5:14b     # Judge model

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the application
export FLASK_APP=app.app:create_app
flask run
```

## README Requirements
- One-paragraph description
- Bullet list explaining Generator → Judge flow
- Setup steps (Ollama + Python + virtual environment)
- Example curl request with response
- Testing section with pytest commands

## Testing Requirements
- Use pytest as the test framework
- Separate fast tests (no LLM calls) from slow tests (with LLM)
- Use `@pytest.mark.slow` for tests that call LLMs
- Flask test client for API endpoint tests (no server needed)
- Test coverage:
  - API endpoint validation (health, conjugate)
  - Request/response structure
  - Error handling (400, 405, 500)
  - Chain creation and JSON output
  - Full integration tests
- Configuration in `pytest.ini`
- Test dependencies: pytest, pytest-timeout

## Explicit Non-Goals (Do Not Implement)
- UI or frontend
- Persistence
- Caching
- Multiple languages
- Streaming responses
- Background jobs
- Performance optimizations

## Definition of Done
- API returns correct Greek present-tense conjugations
- Every request passes through a judge step
- Code is readable and idiomatic Flask
- Architecture clearly demonstrates AI as a Judge
- Comprehensive test suite with >90% pass rate
- Fast tests run in <1 second
- Documentation includes testing instructions

## Design Priority Order
1. Correctness
2. Deterministic behavior
3. Clear separation of generator vs judge
4. Simple, maintainable code

## Implementation Notes

### Model Selection
- **Generator (llama3.1:8b)**: Fast, efficient for initial translation and conjugation
- **Judge (qwen2.5:14b)**: Larger model provides better validation and error correction
- Using different models follows the AI-as-a-Judge pattern where the judge should be at least as capable as the generator

### Prompt Engineering
- Few-shot examples significantly improve accuracy (2 examples per prompt)
- Reference conjugation patterns help judge validate outputs
- JSON format enforcement reduces parsing errors

### Testing Strategy
- Fast tests (no LLM): Unit tests, API validation, structure checks
- Slow tests (with LLM): Integration tests, end-to-end workflows
- Flask test client eliminates need for running server during tests

### Performance Characteristics
- Request latency: 20-45 seconds (generator + judge processing)
- Model memory: ~14GB total (4.9GB + 9GB)
- Fast tests: <1 second
- Full test suite: 3-5 minutes
