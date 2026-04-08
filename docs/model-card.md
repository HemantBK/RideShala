# Model Card — RideShala AI

## Model Details

| Field | Value |
|-------|-------|
| **Primary Model** | Mistral 7B Instruct v0.3 |
| **License** | Apache 2.0 (zero restrictions) |
| **Serving** | vLLM with AWQ 4-bit quantization |
| **Embedding Model** | nomic-embed-text v1.5 (Apache 2.0) |
| **Re-ranker** | ms-marco-MiniLM-L-6-v2 (Apache 2.0) |
| **Agent Framework** | LangGraph (MIT) |
| **Optional Fallbacks** | Claude Sonnet (paid), Groq Llama 3.1 70B (free tier) |

## Intended Use

RideShala's AI system is designed for **motorcycle recommendation and comparison for Indian riders**. It should be used for:

- Personalized bike recommendations based on rider profile
- Side-by-side spec comparisons with trade-off reasoning
- Total Cost of Ownership calculations
- Safety feature analysis
- Ride route planning

## Limitations

- **30-bike database**: Only covers top Indian motorcycles. Not comprehensive.
- **Claimed vs real mileage**: Uses OEM-claimed figures until community data grows.
- **No test rides**: Cannot assess subjective ride quality or feel.
- **Financial estimates**: TCO calculations are approximate. Not financial advice.
- **No real-time pricing**: Uses ex-showroom prices, not actual dealer on-road prices.
- **English only**: Hindi support is Phase 4 (planned, not implemented).

## Training Data

The primary model (Mistral 7B) is **not fine-tuned** on motorcycle data. It uses pre-trained weights with RAG (Retrieval-Augmented Generation) to ground responses in real data from:

- OEM manufacturer websites (30 bikes, factual specs)
- Government data (RTO rates, IRDAI insurance tariffs, IOCL fuel prices)
- User-contributed reviews (with consent, CC BY-SA 4.0)
- User-tracked mileage and service costs

## Evaluation

**Framework:** RAGAS (Apache 2.0)
**Test Set:** 49 curated Q&A pairs across 6 categories

| Metric | Target | Current |
|--------|--------|---------|
| Faithfulness | > 0.85 | Pending (requires running LLM) |
| Answer Relevancy | > 0.80 | Pending |
| Context Precision | > 0.75 | Pending |
| Context Recall | > 0.70 | Pending |
| Data Availability | > 80% | ~85% (30 bikes cover most test questions) |

## Bias & Safety

### Safety Guardrails (hardcoded, LLM cannot override)
- Always recommends dual-channel ABS
- Always recommends proper riding gear (helmet, gloves, jacket, boots)
- Never suggests disabling safety features
- Never encourages speeding or illegal modifications
- Adds financial disclaimers to all TCO/EMI calculations

### Bias Monitoring (planned)
- Quarterly automated check: does AI favor certain brands?
- Compare brand mentions against market share
- Flag over/under-representation > 20%
- Publish results in public bias report

### Known Biases
- Database skews toward 150-450cc segment (most popular in India)
- Under-represented: electric bikes, scooters, 600cc+ bikes
- Royal Enfield over-represented (5 models) due to market share

## Ethical Considerations

- **No hidden sponsorships**: Recommendations are never influenced by money
- **Source citations**: Every factual claim links to its data source
- **"I don't know"**: AI explicitly states when data is insufficient
- **Confidence scores**: Planned for future versions
- **Open source**: Anyone can audit the recommendation logic

## Cost

- **Default (free)**: Mistral 7B via vLLM on self-hosted GPU. Zero API cost.
- **Optional (paid)**: Claude API available for premium reasoning. Not required.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-04-08 | Initial release: 30 bikes, 8 agents, hybrid RAG, moderation |
