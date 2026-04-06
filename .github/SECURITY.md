# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in RideShala, please report it responsibly:

**Email:** security@rideshala.in

**Do NOT** open a public GitHub issue for security vulnerabilities.

We will:
- Acknowledge your report within 48 hours
- Provide an estimated fix timeline within 5 business days
- Credit you in the security advisory (unless you prefer anonymity)

## Supported Versions

| Version | Supported |
|---------|-----------|
| Latest main branch | Yes |
| Older releases | Best effort |

## Security Practices

- All dependencies are scanned via `pip-audit` and `npm audit` in CI
- API keys are never committed to git (enforced via `.gitignore` and CI checks)
- User inputs are validated and sanitized before processing
- LLM prompts use system/user message separation to prevent injection
- Rate limiting prevents abuse
- CORS is configured with explicit domain whitelist
