# RideShala

**Open-source AI motorcycle advisor for Indian riders. Free. Self-hosted. Community-owned.**

Built with Mistral 7B | vLLM | LangGraph | FastAPI | Next.js

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Data: CC BY-SA 4.0](https://img.shields.io/badge/Data-CC%20BY--SA%204.0-blue.svg)](DATA_LICENSE)
[![CI](https://github.com/HemantBK/RideShala/actions/workflows/ci.yml/badge.svg)](https://github.com/HemantBK/RideShala/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](.github/CONTRIBUTING.md)

---

Tell RideShala about yourself — height, budget, city, riding style — and it recommends the perfect bike with full reasoning and source citations. No spec tables. No guesswork.

```
You:  "5'7, back pain, Bangalore commute 25km, weekend Coorg trips, budget 2.5L"

RideShala: "I recommend the Meteor 350 because:
           - 765mm seat = your feet flat on ground at 5'7
           - Cruiser posture = less back strain than a roadster
           - 15L tank = Bangalore to Coorg without refueling
           - Rs 2.19L = Rs 31K under budget for accessories

           But: 20 bhp may feel slow on Shiradi Ghat.
           Alternative: Hero Mavrick 440 (27 bhp, Rs 2.15L)

           [Sources: royalenfield.com specs, 847 user reviews on RideShala]"
```

## Quick Start

```bash
git clone https://github.com/HemantBK/RideShala.git
cd RideShala
cp .env.example .env
cd infra && docker compose --profile gpu up -d
```

Open http://localhost:3000 — no API keys needed. Everything runs locally.

## What Makes It Different

- **Understands YOU** — personalized to your height, city, budget, riding style
- **Cites every source** — no black-box recommendations
- **Real-world data** — actual mileage and service costs tracked by real owners
- **Warns you** — hardcoded safety rules the AI cannot override
- **6 AI agents** — research, comparison, safety, finance, ride planning, guardrails
- **Moderation pipeline** — plagiarism detection, toxicity filter, quality checks on all reviews
- **Community contributions** — Wikipedia-style spec editing with OEM source verification
- **100% free** — Mistral 7B (Apache 2.0) on your GPU, zero paid APIs
- **100% legal** — every data point has a documented source, nothing scraped
- **100% open** — MIT code, CC BY-SA data, community-owned

## Features

| Feature | Description |
|---------|------------|
| AI Chat | Conversational bike advisor with SSE streaming |
| Smart Compare | AI-powered comparison with trade-off reasoning, not just spec tables |
| TCO Calculator | 5-year ownership cost using real government data (RTO, IRDAI, IOCL) |
| Ride Planner | Route planning with fuel stops, weather, and safety tips (OSRM + Open-Meteo) |
| Mileage Tracker | Community-tracked real-world fuel economy from actual fill-ups |
| Service Tracker | Real service costs reported by owners — dealer vs local breakdown |
| Review System | Moderated user reviews with plagiarism detection and consent tracking |
| Spec Contributions | Community can submit corrections with OEM source verification |
| Safety Guardrails | Hardcoded rules the AI cannot override — always recommends ABS, gear |
| 30 Bikes | Pre-loaded database of top Indian motorcycles with OEM-sourced specs |

## Documentation

| Doc | What's inside |
|-----|--------------|
| **[Architecture](docs/architecture.md)** | System design, diagrams, tech stack, design decisions |
| **[AI Pipeline](docs/ai-pipeline.md)** | LLM routing, RAG, multi-agent system, prompts, evaluation |
| **[Model Card](docs/model-card.md)** | Model details, limitations, bias, safety, evaluation metrics |
| **[API Reference](docs/api.md)** | All 21 endpoints with curl examples |
| **[Setup Guide](docs/setup.md)** | Full development environment setup |
| **[Deployment](docs/deployment.md)** | Docker, production, monitoring, backups |
| **[Scaling Guide](docs/scaling.md)** | Phase 4 roadmap — Flutter, fine-tuning, K8s, Hindi support |
| **[Legal Compliance](docs/legal-compliance.md)** | DPDP Act, copyright, data sources |
| **[Contributing](.github/CONTRIBUTING.md)** | How to contribute code, data, translations |

## License

Code: [MIT](LICENSE) | Data: [CC BY-SA 4.0](DATA_LICENSE) | Models: [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES)
