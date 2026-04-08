# Scaling Guide (Phase 4)

This document covers the future scaling roadmap. Phases 1-3 are complete — the system is functional with 30 bikes, AI agents, moderation, tracking, and community contributions. Phase 4 is about scaling to production.

## Roadmap

| Task | Priority | Effort | Description |
|------|----------|--------|-------------|
| Flutter mobile app | High | 4-6 weeks | iOS + Android app using the existing API |
| Expand bike database | High | Ongoing | Community-driven: 30 → 200+ bikes |
| QLoRA fine-tuning | Medium | 2 weeks | Fine-tune Mistral 7B on motorcycle domain after 10K+ interactions |
| A/B testing framework | Medium | 1 week | Traffic splitting between base and fine-tuned models |
| Hindi language support | Medium | 2 weeks | Prompts + UI in Hindi, Hinglish query handling |
| Kubernetes deployment | Medium | 2 weeks | K3s manifests for multi-node production |
| Public API with key management | Medium | 1 week | API keys, usage quotas, developer portal |
| MLflow model tracking | Low | 1 week | Experiment tracking, model versioning |
| Embedding drift monitoring | Low | 1 week | Detect when review distributions shift |
| Bias audits | Low | Ongoing | Quarterly brand favoritism checks |

## Flutter Mobile App

The API is already built — the mobile app consumes the same endpoints.

```
apps/mobile/
├── lib/
│   ├── main.dart
│   ├── screens/
│   │   ├── home_screen.dart          Chat interface
│   │   ├── compare_screen.dart       Side-by-side comparison
│   │   ├── bike_detail_screen.dart   Full specs page
│   │   └── settings_screen.dart      Privacy, consent manager
│   ├── services/
│   │   └── api_service.dart          HTTP client for RideShala API
│   └── models/
│       ├── bike.dart
│       └── review.dart
└── pubspec.yaml
```

Key features:
- SSE streaming chat (same as web)
- Offline mode for saved comparisons
- Push notifications for ride weather alerts
- Camera integration for uploading bike photos

## Fine-Tuning Pipeline

After 10,000+ user interactions with feedback (thumbs up/down):

**Method:** QLoRA (4-bit quantization + LoRA adapters)

```bash
# Tools: Hugging Face TRL + PEFT (both Apache 2.0, free)
pip install trl peft transformers datasets

# Training data: user queries + approved responses from usage_logs
# Hardware: single A100 or 2x A10G on RunPod (~$10-20 per training run)
# Evaluation: RAGAS on golden test set (49 Q&A pairs)
```

**Training loop:**
1. Export 10K+ (query, response, rating) pairs from usage_logs
2. Filter to highly-rated responses (thumbs up)
3. Format as instruction-following dataset
4. QLoRA fine-tune Mistral 7B (4-bit base + LoRA adapters)
5. Evaluate on golden test set using RAGAS
6. A/B test: route 10% traffic to fine-tuned model
7. If RAGAS scores improve AND user satisfaction improves → promote

**Model storage:** MLflow for versioning. Keep base model + LoRA adapters (< 100MB per fine-tune).

## A/B Testing Framework

```python
# In LLM router — configurable traffic split
AB_TEST_CONFIG = {
    "base_model": {"weight": 0.9, "model": "mistralai/Mistral-7B-Instruct-v0.3"},
    "finetuned": {"weight": 0.1, "model": "rideshala/mistral-7b-bikes-v1"},
}

# Track per-variant metrics:
# - User satisfaction (thumbs up/down ratio)
# - RAGAS scores (faithfulness, relevancy)
# - Response latency
# - Token efficiency
```

## Hindi Language Support

### Prompts
- Duplicate all 6 system prompts with Hindi versions
- Add Hinglish detection: "yeh bike kaisi hai?" → route to Hindi prompt
- Auto-detect language from user query using vLLM

### UI
- Language toggle in Next.js header
- Hindi translations for all UI strings
- RTL is not needed (Hindi is LTR)

### Data
- Hindi bike names are the same (Royal Enfield = रॉयल एनफील्ड)
- User reviews can be submitted in Hindi
- Hindi reviews embedded separately in Qdrant (same collection, `language` payload field)

## Kubernetes Deployment

For 10,000+ concurrent users:

```yaml
# infra/k8s/
├── namespace.yaml
├── api-deployment.yaml          # FastAPI (HPA: 2-10 replicas)
├── api-service.yaml
├── web-deployment.yaml          # Next.js (2 replicas)
├── web-service.yaml
├── vllm-deployment.yaml         # GPU node (1 replica, dedicated)
├── vllm-service.yaml
├── ingress.yaml                 # Nginx ingress with TLS
├── configmap.yaml               # Non-secret environment vars
├── secrets.yaml                 # API keys (if optional paid providers enabled)
└── hpa.yaml                     # Horizontal Pod Autoscaler for API
```

**Key decisions:**
- Use K3s (lightweight Kubernetes) for cost efficiency
- vLLM on dedicated GPU node (not autoscaled — GPU is expensive)
- FastAPI pods autoscale based on CPU/request count
- PostgreSQL on managed service (Supabase or Neon) at scale
- Qdrant with persistent volumes on SSD

## Public API

For third-party developers building on RideShala data:

```
POST /api/v1/developer/register    → Get API key
GET  /api/v1/developer/usage       → Check quota

# All existing endpoints work with API key:
GET /api/v1/specs?api_key=rsk_xxx
POST /api/v1/compare?api_key=rsk_xxx
```

**Quotas:**
- Free tier: 1,000 requests/day
- Data attribution required: "Data from RideShala (rideshala.in)"
- API responses licensed under CC BY 4.0 (no share-alike for API)
- Bulk database download: CC BY-SA 4.0 (share-alike for bulk)

## MLflow Model Tracking

```bash
pip install mlflow  # Apache 2.0, free

# Log every training run:
mlflow.log_params({"base_model": "mistral-7b", "lora_rank": 16, "epochs": 3})
mlflow.log_metrics({"faithfulness": 0.89, "relevancy": 0.85})
mlflow.log_artifact("lora_adapters/")
```

Track: training data version, hyperparameters, RAGAS scores, user satisfaction metrics, inference latency.

## Embedding Drift Monitoring

Monthly check:
1. Sample 100 new reviews
2. Embed them
3. Compare distribution (centroid, spread) against training-time distribution
4. If drift > threshold → alert + re-evaluate RAG quality
5. If RAGAS scores drop → trigger re-indexing or model update

## Bias Audits

Quarterly automated check:
1. Run 50 recommendation queries with neutral profiles (no brand mentioned)
2. Count brand mentions in AI responses
3. Compare against actual market share
4. If any brand is over/under-represented by > 20% → investigate
5. Publish results in a public bias report on GitHub

## Cost Projections at Scale

| Users | Infrastructure | Monthly Cost |
|-------|---------------|-------------|
| < 1,000 | Docker Compose on single VPS + GPU | Rs 2,000 - 5,000 |
| 1,000 - 10,000 | K3s cluster + dedicated GPU node | Rs 10,000 - 20,000 |
| 10,000 - 100,000 | Multi-node K8s + managed DB + 2 GPUs | Rs 30,000 - 50,000 |

**Funding options:**
- GitHub Sponsors
- Open Collective (transparent community funding)
- Google Summer of Code (student contributors)
- FOSS United India (Indian open source grants)
- MLH Fellowship (student contributors)

All infrastructure costs are for self-hosted hardware. Zero paid API costs (Mistral 7B via vLLM is free).
