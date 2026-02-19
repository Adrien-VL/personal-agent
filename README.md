# personal-agent

## Ruff Commands

- **Lint code**: `uv run ruff check .`
- **Format code**: `uv run ruff format .`
- **Fix linting issues**: `uv run ruff check --fix .`

## Testing Commands

- **Run all tests**: `uv run pytest tests/`
- **Run unit tests only**: `uv run pytest tests/unit/` or `uv run pytest -m unit`
- **Run integration tests only**: `uv run pytest tests/integration/` or `uv run pytest -m integration`
- **Run e2e tests only**: `uv run pytest tests/e2e/` or `uv run pytest -m e2e`
- **Run tests with verbose output**: `uv run pytest -v`

## Test Structure

```
tests/
├── config.py              # Test configuration (API keys, model configs)
├── unit/                 # Fast tests, no external dependencies
│   ├── test_model.py
│   ├── test_ghost.py
│   └── test_shell.py
├── integration/          # Real API integration tests
│   └── test_glm.py
└── e2e/                 # Full system tests
    └── test_e2e.py
```

## Directory Structure

```
personal-agent/
├── agent/
│   ├── sources/            # Model provider implementations
│   │   └── glm.py       # Z.AI GLM provider
│   ├── enhancers/          # Future: Shell context enhancer implementations
│   │   └── *.py         # RAG, web search, persistent memory
│   ├── processors/          # Future: Shell response processors
│   │   └── *.py         # Output transformations, formatting
│   ├── model.py           # BaseModel abstract class and dataclasses
│   ├── ghost.py           # Internal processing engine
│   └── shell.py           # Sensory/motor layer
├── tests/                 # Testing infrastructure
├── knowledge/             # Knowledge base documents
├── main.py               # CLI entry point
└── pyproject.toml         # Project configuration
```

**Future Directories:**
- `agent/enhancers/` - Context enhancer implementations (similar to `sources/`)
- `agent/processors/` - Response processor implementations (similar to `sources/`)

## Testing Pyramid

We follow a 70/20/10 testing pyramid for optimal balance of speed and coverage:

```
         E2E (10%)
        /          \
       /            \
      /              \
     /   Integration (20%)
    /                    \
   /                      \
  /                        \
 /                          \
/_____________________________\
            Unit (70%)
```

**Unit Tests (70%)** - Fast, isolated, no external dependencies
- Test individual components in isolation
- Mock external dependencies
- Execute in milliseconds
- Example: `Ghost` with mock model, `InputPort` with mock enhancers

**Integration Tests (20%)** - Test real component integration
- Real API calls to external services
- Verify actual behavior, not just mocks
- Require API keys (skipped if unavailable)
- Example: Real GLM API calls with actual responses

**E2E Tests (10%) - Full system integration
- Test entire flow end-to-end
- Catch integration issues between components
- Require all dependencies
- Example: Ghost → Shell → GLM → full conversation

**Why this balance?**
- Fast feedback: Unit tests run instantly
- Real verification: Integration tests catch real issues
- System validation: E2E tests verify everything works together

## General Philosophy

### Simplicity Over Complexity
- Keep directory structure shallow (max 3 levels)
- Prefer clear naming over clever abstractions
- Build what you need, not what you might need
- If it's hard to understand, it's probably wrong

### Test What Matters
- Test paths through code, not every line
- Focus on behavior, not implementation details
- Don't test private methods
- If a test is testing the test framework, delete it

### Pragmatic Dependencies
- Use standard library when possible
- Prefer minimal, focused libraries
- Avoid framework lock-in
- Easy to add, easy to remove

### Code as Communication
- Code should explain itself
- Comments are for "why", not "what"
- Naming matters more than documentation
- Clean code is better than clever code

### Iterative Improvement
- Ship working code, not perfect code
- Refactor when you understand the problem
- Delete code that isn't used
- Technical debt is okay if it serves a purpose

### Tooling Should Get Out of the Way
- Fast feedback loops (<1 second for unit tests)
- Linting/formatting should be automatic
- Debugging should be straightforward
- Convention over configuration where it makes sense

## Environment Variables

- `ZAI_API_KEY`: Required for integration and e2e tests (Z.AI API key)

## Agent Configuration (Future)

The agent architecture will be guided through markdown configuration files in the project root:

- **GHOST.md** - Internal processing configuration
  - Reasoning strategies and thought patterns
  - Internal state management rules
  - Context handling and memory integration

- **SHELL.md** - Sensory and motor layer configuration
  - Input/output port definitions
  - Context enhancer implementations (RAG, web search, persistent memory)
  - External tool integrations and wrappers

- **ENVIRONMENT.md** - Environment context and configuration
  - Model selection and provider settings
  - Available tools and capabilities
  - User(s) information and preferences
  - System prompts and behavioral constraints
  - Session context and runtime parameters

These files will serve as both documentation and runtime configuration, allowing the agent to understand its own architecture and capabilities through self-reflection.

