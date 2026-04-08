# Contributing to RideShala

Thank you for your interest in contributing to RideShala! Every contribution helps Indian riders make better bike-buying decisions.

## Ways to Contribute

### Non-code contributions (no programming needed)

- **Add bike specs**: Read specs from manufacturer websites and submit as a PR
- **Verify data**: Cross-check existing specs against OEM sources
- **Report bugs**: Open an issue describing what went wrong
- **Suggest features**: Share your ideas in GitHub Discussions
- **Translations**: Help us support regional Indian languages — contribute translations for your language

### Code contributions

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `cd services/api && pytest`
5. Commit with conventional commits: `git commit -m "feat: add new feature"`
6. Push and open a Pull Request

### Commit message format

```
feat: add bike comparison endpoint
fix: correct mileage calculation for diesel bikes
docs: update API documentation
refactor: simplify LLM router fallback logic
test: add tests for hybrid search
chore: update dependencies
```

## Development Setup

See the [Quick Start](../README.md#quick-start) section in README.md.

## Code Standards

- **Python**: Use type hints, format with `ruff`, docstrings on public functions
- **TypeScript**: ESLint + Prettier configuration provided
- **Tests**: New features should include tests
- **Security**: Never commit API keys, passwords, or secrets

## Data Contribution Rules

When adding bike specifications:
1. Source MUST be an official manufacturer website
2. Include the source URL in your PR description
3. Only add factual data (specs, prices) — never copy marketing text
4. All contributed data is licensed under CC BY-SA 4.0

## Review Process

1. All PRs require at least one review from a maintainer
2. CI must pass (linting, tests, security audit)
3. Data PRs require source verification
4. We aim to review PRs within 48 hours

## Questions?

Open a GitHub Discussion or ask in the PR — we're happy to help!
