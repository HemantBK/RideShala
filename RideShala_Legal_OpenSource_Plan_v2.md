# RideShala — Open Source AI Bike Comparison App
## Legally Safe, Free, Zero Compliance Issues

> **License:** MIT (fully open source, free forever)  
> **Date:** April 2026  
> **Principle:** Every byte of data is either self-created, user-contributed, officially published by manufacturers, or from open/free APIs. Nothing scraped. Nothing stolen. Nothing grey-area.

---

## Table of contents

1. [Golden rule: legal-first data strategy](#1-golden-rule-legal-first-data-strategy)
2. [What is legal vs illegal (clear chart)](#2-what-is-legal-vs-illegal)
3. [Legal data sources (exactly where every data point comes from)](#3-legal-data-sources)
4. [Product overview](#4-product-overview)
5. [AI features that make us different](#5-ai-features-that-make-us-different)
6. [RAG architecture (legally clean)](#6-rag-architecture-legally-clean)
7. [Agentic AI system](#7-agentic-ai-system)
8. [Generative AI features](#8-generative-ai-features)
9. [Safety, trust & responsibility](#9-safety-trust--responsibility)
10. [Compliance checklist](#10-compliance-checklist)
11. [Tech stack (all open source / free tier)](#11-tech-stack)
12. [System architecture](#12-system-architecture)
13. [Data pipeline (100% legal)](#13-data-pipeline)
14. [MVP roadmap](#14-mvp-roadmap)
15. [Open source community strategy](#15-open-source-community-strategy)
16. [Cost (zero to minimal)](#16-cost)
17. [Risks & mitigations](#17-risks--mitigations)
18. [UPGRADED: vLLM production LLM serving](#18-vllm-production-llm-serving)
19. [UPGRADED: Claude API integration](#19-claude-api-integration)
20. [UPGRADED: LangGraph flow orchestration](#20-langgraph-flow-orchestration)
21. [UPGRADED: Hybrid RAG pipeline](#21-hybrid-rag-pipeline)
22. [UPGRADED: Production readiness](#22-production-readiness)
23. [UPGRADED: Legal compliance fixes](#23-legal-compliance-fixes)
24. [UPGRADED: AI skills showcase](#24-ai-skills-showcase)
25. [UPGRADED: Monorepo project structure](#25-monorepo-project-structure)
26. [UPGRADED: Updated roadmap](#26-updated-roadmap)

---

## 1. Golden rule: legal-first data strategy

```
╔══════════════════════════════════════════════════════════════╗
║                     THE GOLDEN RULE                         ║
║                                                              ║
║  We NEVER scrape any third-party website.                    ║
║  We NEVER copy reviews, images, or content from other apps.  ║
║  We NEVER collect personal data without explicit consent.     ║
║  We NEVER use copyrighted content without permission.         ║
║                                                              ║
║  Every data point has a LEGAL SOURCE documented.             ║
║  Every image has a LICENSE attached.                         ║
║  Every user contribution has CONSENT recorded.               ║
║                                                              ║
║  If we can't get data legally → we don't use it.             ║
║  If it's grey area → we skip it entirely.                    ║
╚══════════════════════════════════════════════════════════════╝
```

---

## 2. What is legal vs illegal

### ✅ Completely legal (we DO this)

| Data | Source | Why it's legal |
|---|---|---|
| Bike specifications (cc, bhp, torque, weight) | Manufacturer websites (official specs pages) | Facts cannot be copyrighted. OEMs publish specs publicly for buyers |
| Ex-showroom prices | Manufacturer websites + press releases | Publicly advertised commercial information |
| Bike images | OEM media kits / press releases | Manufacturers provide press images for editorial use |
| User-written reviews | Our own users write them on our platform | We own the platform, users grant us license |
| Community-contributed specs | Volunteer contributors (like Wikipedia model) | Contributors explicitly license under CC BY-SA |
| YouTube video links (not transcripts) | YouTube oEmbed/public URLs | Linking is legal everywhere |
| Government data (RTO rates, emission norms) | Parivahan.gov.in, state transport sites | Public government data, free to use |
| Fuel prices | IOCL/BPCL official published prices | Public pricing data |
| Open APIs with free tier | API Ninjas Motorcycle API, etc. | Explicitly allowed by their terms |
| AI-generated analysis | Our own AI models analyzing our own data | We own the output of our own analysis |

### ❌ Illegal / risky (we NEVER do this)

| Data | Source | Why it's illegal |
|---|---|---|
| Scraping BikeWale/BikeDekho databases | Web scraping | Violates their ToS + Copyright Act Section 13 |
| Copying user reviews from other platforms | Copy-paste or scraping | Copyright belongs to platform/user |
| Using images from other bike websites | Downloading their images | Copyright infringement |
| Scraping YouTube transcripts in bulk | YouTube transcript extraction | Violates YouTube ToS Section 5 |
| Copying expert review text | From Autocar, ZigWheels, etc. | Copyrighted editorial content |
| Collecting user location without consent | Background tracking | Violates DPDP Act 2023 |
| Storing user data without purpose limitation | Over-collection | Violates DPDP Act 2023 |

### ⚠️ Grey area (we AVOID entirely)

| Data | Why we skip it |
|---|---|
| Reddit API data | Reddit changed API terms in 2023, commercial use restricted |
| YouTube Data API transcripts | API allows metadata, but transcript extraction for AI training is debated |
| Google Reviews | Google ToS prohibits systematic extraction |
| Cached/archived web pages | Even Wayback Machine content has copyright debates |

---

## 3. Legal data sources

### Source 1: OEM (manufacturer) websites — SPECS & PRICES

**What we take:** Specifications, ex-showroom prices, variant details, color options  
**How:** Manual data entry by contributors + periodic manual verification  
**Legal basis:** Facts (cc, bhp, weight, dimensions) are not copyrightable. Prices are publicly advertised.  
**Sources:**
- royalenfield.com/in/en/motorcycles/
- honda2wheelersindia.com
- heromotocorp.com
- bajajauto.com/bikes
- tvsmotor.com
- triumphind.in
- ktmindia.com
- jawamotorcycles.com
- harley-davidson.com/in

**Process:** Human contributors (community volunteers) read the OEM page and type specs into our structured database. This is research and fact compilation — identical to what Wikipedia does. We do NOT copy descriptive text, marketing copy, or images from these pages.

### Source 2: OEM press/media kits — IMAGES

**What we take:** Official bike images  
**How:** Download from manufacturer media rooms (most OEMs have press image sections)  
**Legal basis:** Press images are released for editorial/media use  
**Sources:**
- Royal Enfield: media.royalenfield.com
- Honda: hondanews.com
- Triumph: triumphmotorcycles.com/press
- Most OEMs provide media kits on request via email

**Fallback:** If no press images available:
- Commission original photos from community members (they photograph their own bikes)
- Use AI-generated representative illustrations (clearly labeled as "AI illustration, not actual photo")
- User-submitted photos (user grants license on upload)

### Source 3: Government / public data — PRICES, RTO, INSURANCE

| Data | Source | Legal basis |
|---|---|---|
| RTO charges by state | parivahan.gov.in, state transport websites | Public government data |
| Insurance rates | IRDAI published tariff rates | Public regulatory data |
| Fuel prices | iocl.com daily price, bpcl.co.in | Publicly published |
| Emission norms (BS-VI) | araiindia.com, MoRTH notifications | Public government data |
| Road tax calculator | State-wise formulas (publicly documented) | Public government data |

### Source 4: Free/open APIs — SUPPLEMENTARY SPECS

| API | What it provides | Terms | Cost |
|---|---|---|---|
| API Ninjas Motorcycle API | Global motorcycle specs | Free tier: 10,000 calls/month | Free |
| OpenWeather API | Weather data (for ride planning) | Free tier: 1,000 calls/day | Free |
| Google Maps Platform | Dealer locations, directions | $200 free credit/month | Free tier |
| Nominatim (OpenStreetMap) | Geocoding, location search | Free, open source | Free |

### Source 5: User-generated content (OUR OWN PLATFORM)

This is our **most important and legally cleanest** data source.

**What users contribute:**
- Written reviews of bikes they own
- Mileage reports (actual fuel consumption tracking)
- Service cost logs (what they paid at service centers)
- Photos of their own bikes
- Ratings (comfort, performance, mileage, value)
- Long-term ownership reports
- Modification/accessory reviews

**Legal protection:**
```
USER CONTRIBUTION AGREEMENT (shown at signup):

"By submitting content to RideShala, you grant RideShala a worldwide, 
royalty-free, non-exclusive license to use, display, and distribute 
your content on our platform and in our AI systems. You retain 
ownership of your content and can delete it anytime.

Your content will be licensed under Creative Commons BY-SA 4.0, 
meaning anyone can use it with attribution. This helps the 
motorcycle community while protecting your rights.

You confirm that:
- The content is your original work
- Photos are taken by you or you have permission
- You are not copying from other websites
- Your review reflects your genuine experience"
```

### Source 6: Community-maintained open database (Wikipedia model)

We create and maintain an **open motorcycle specifications database** — similar to how Wikipedia maintains encyclopedia articles.

**How it works:**
- Anyone can contribute specs (with OEM source link required)
- Changes are reviewed before going live (like Wikipedia edits)
- All data is licensed under **CC BY-SA 4.0** (Creative Commons)
- Full edit history maintained (transparency)
- Anyone can download the entire database (truly open)

**This becomes a public good** — other developers can use it too. This is our moat: the most accurate, community-verified, open motorcycle database for India.

---

## 4. Product overview

### What is RideShala?

An **open-source, AI-powered bike comparison app** that helps Indian riders find the perfect bike based on their unique needs — height, weight, budget, riding style, commute, city, and more.

### How we're different

```
BikeWale/BikeDekho:  Spec database → Filters → Static table → User decides alone
                     (data dump, no reasoning, overwhelming)

RideShala:             Conversation → Understands YOU → Researches → Reasons → Recommends
                     (personalized, explainable, trustworthy, open source)
```

### Core value proposition

| For riders | What we give them |
|---|---|
| First-time buyers | "I don't know bikes. Just tell me what's best for MY situation." |
| Upgraders | "I have a Pulsar 150. What's a meaningful upgrade for 2L?" |
| Confused between 2-3 bikes | "Meteor vs Guerrilla vs CB350 — FOR ME, which one?" |
| Long-term owners | "Track my service costs, remind me about maintenance" |

---

## 5. AI features that make us different

### 5.1 Conversational AI advisor

Users describe their needs in natural language. The AI recommends bikes with full reasoning.

```
User: "5'7, back pain, Bangalore commute 25km, weekend Coorg trips, budget 2.5L"

AI: "I recommend the Meteor 350 for you because:
     - 765mm seat = comfortable for 5'7 (your feet will be flat)
     - Cruiser posture = less back strain than roadsters
     - 15L tank = Bangalore to Coorg without refueling
     - ₹2.19L fits your budget with room for accessories
     
     ⚠️ Note: 20 bhp may feel slow on Shiradi Ghat inclines.
     If that matters, the Hero Mavrick 440 (27 bhp) at ₹2.15L
     is worth test riding.
     
     [Sources: Specs from royalenfield.com, comfort rating from
      847 user reviews on our platform]"
```

**Key difference from ChatGPT/Gemini:** Our AI is grounded in REAL, VERIFIED data from our own database — not training data that may be outdated or hallucinated.

### 5.2 Smart comparison (not just spec tables)

Instead of showing two columns of numbers, the AI explains:
- "The Guerrilla has double the Meteor's power, but you'll pay ₹3,000 more per year in service costs"
- "The CB350 has traction control — crucial for your Bangalore monsoon commute"
- "The Meteor's 765mm seat is 35mm lower than the CB350 — significant for your height"

### 5.3 AI review synthesizer (from OUR OWN user reviews)

Aggregates insights from thousands of reviews on OUR platform:

```
RE Meteor 350 — Review Summary (from 2,847 reviews on RideShala)

WHAT OWNERS LOVE:
- Comfort on long rides (89% positive mentions)
- Low seat height (94% positive)
- Tripper navigation (78% positive)

COMMON COMPLAINTS:
- Stiff rear suspension for pillion (67% negative)
- Underpowered above 100 km/h (54% negative)

MILEAGE REALITY: Avg 33.2 kpl (from 1,204 tracked fill-ups)
SERVICE COST REALITY: Avg ₹2,847 per service (from 623 logged services)
```

**Legally clean:** All data comes from our own users, with their explicit consent.

### 5.4 Total cost of ownership (TCO) calculator

AI calculates personalized 5-year cost:
- Purchase price (from OEM published price)
- RTO charges (from government rate tables)
- Insurance (from IRDAI tariff rates)
- Fuel (user's commute × current petrol price from IOCL)
- Service (from user-reported service logs on our platform)
- Tyre replacement (from user reports)
- Resale estimate (from user-reported sale prices on our platform)

**Every data point has a legal source. No scraping needed.**

### 5.5 AI safety advisor

- Flags bikes missing dual-channel ABS
- Warns about known issues (from user reports on our platform)
- Helmet and gear recommendations
- Rain/night riding safety tips
- Emergency service center finder (Google Maps API)

### 5.6 Crowd-sourced dealer price tracker

Users voluntarily share their on-road quotes from dealers:
- "I got Meteor 350 Stellar for ₹2.42L on-road in Bangalore from XYZ dealer"
- AI aggregates anonymous price data to show fair price ranges
- No dealer partnership needed — pure crowd-sourced data

### 5.7 Ride planner

- Fuel stops based on your bike's tank + mileage
- Weather from OpenWeather API
- Route from OpenStreetMap / Google Maps API
- Service centers along the route (user-submitted locations)

---

## 6. RAG architecture (legally clean)

### Data flow (every source is legal)

```
LEGAL DATA SOURCES
├── Our PostgreSQL DB (community-maintained specs)
├── Our Vector DB (user-written reviews, embeddings)
├── Free APIs (fuel price, weather, maps)
├── Government data (RTO, insurance rates)
└── OEM published specs (manually entered)
        │
        ▼
   ┌────────────┐
   │ RAG Engine │
   ├────────────┤
   │ 1. Query understanding (LLM)
   │ 2. Route to correct data source
   │ 3. Retrieve relevant data
   │ 4. Generate response with citations
   │ 5. Safety guardrail check
   │ 6. Return with sources + confidence
   └────────────┘
        │
        ▼
   User sees: Answer + "Source: 847 user reviews on RideShala"
              (never "Source: BikeWale" or "Source: scraped data")
```

### Vector database (for review search)

```
Collection: user_reviews (OUR OWN USER DATA)
├── Fields: review_text, embedding, bike_model, user_id,
│           sentiment, verified_owner, date, aspect,
│           mileage_reported, service_cost_reported
├── Embedding model: all-MiniLM-L6-v2 (open source, free)
│   OR nomic-embed-text (open source)
├── Vector DB: ChromaDB (open source, free) 
│   OR Qdrant (open source, free self-hosted)
├── Chunk size: 256 tokens
└── All data is user-contributed with CC BY-SA 4.0 license
```

### What goes into RAG context

```
For query: "Is Meteor 350 good for long rides?"

Retrieved context (all from our own legal data):
├── 23 user reviews mentioning "long ride" + "Meteor 350" [our platform]
├── Spec data: seat height 765mm, tank 15L, weight 191kg [from OEM site]
├── Average mileage: 33.2 kpl [from 1,204 user fill-up logs on our platform]
├── Comfort rating: 4.3/5 [from 2,847 reviews on our platform]
└── Common long-ride issues reported by users [our platform]

NOT retrieved (we don't have this data and that's OK):
├── BikeWale reviews ← NOT OUR DATA
├── YouTube transcripts ← NOT OUR DATA
├── Autocar expert review ← NOT OUR DATA
└── Forum posts ← NOT OUR DATA
```

**The trade-off:** We'll have less data initially than if we scraped everything. But our data is **100% legal, 100% verified, and 100% ours**. Quality beats quantity.

---

## 7. Agentic AI system

### Agent architecture (same as before, but legally clean data)

```
ORCHESTRATOR AGENT
├── Research Agent
│   ├── Searches OUR specs database (PostgreSQL)
│   ├── Searches OUR review database (Vector DB)  
│   ├── Calls free APIs (fuel price, weather, maps)
│   └── NEVER scrapes external websites
│
├── Analysis Agent
│   ├── Compares specs against user profile
│   ├── Calculates TCO from legal data sources
│   └── Generates personalized scores
│
├── Safety Agent
│   ├── Checks our user-reported issues database
│   ├── Validates safety features from OEM specs
│   └── Generates riding safety tips
│
├── Finance Agent
│   ├── EMI calculator (standard math formulas)
│   ├── Insurance estimate (IRDAI published rates)
│   ├── RTO calculator (government published rates)
│   └── Resale estimate (from user-reported sales on our platform)
│
├── Location Agent
│   ├── Google Maps / OpenStreetMap for dealer search
│   ├── User-submitted service center locations
│   └── OpenWeather for ride planning
│
└── Content Agent
    ├── Generates comparison reports
    ├── Creates shareable cards
    └── All from OUR legal data only
```

### Tool definitions (all legally clean)

```python
# Every tool the agent can use — all legally safe

tools = [
    # OUR OWN DATABASE
    "search_bike_specs",      # PostgreSQL — community-maintained
    "search_user_reviews",    # Vector DB — user-contributed
    "get_mileage_data",       # Aggregated from user fill-up logs
    "get_service_cost_data",  # Aggregated from user service logs
    "get_user_ratings",       # Star ratings from our platform
    
    # FREE / OPEN APIs
    "get_fuel_price",         # IOCL published data
    "get_weather",            # OpenWeather free tier
    "search_location",        # Google Maps / OSM
    "calculate_route",        # Google Maps / OSRM (open source)
    
    # CALCULATORS (pure math, no external data needed)
    "calculate_emi",          # Standard EMI formula
    "calculate_rto",          # Government rate tables
    "calculate_insurance",    # IRDAI tariff-based
    "calculate_tco",          # Combines above data
    
    # NEVER AVAILABLE — these tools DO NOT EXIST in our system
    # "scrape_bikewale"       ← DOES NOT EXIST
    # "scrape_bikedekho"      ← DOES NOT EXIST
    # "fetch_youtube_transcript" ← DOES NOT EXIST
    # "scrape_reviews"        ← DOES NOT EXIST
]
```

---

## 8. Generative AI features

### 8.1 Personalized comparison reports
- AI generates custom HTML/PDF reports from OUR data
- Shareable via link or download
- Contains only data from legal sources (our DB + OEM specs)

### 8.2 AI-generated bike illustrations
- For color visualization, use open-source Stable Diffusion
- Clearly labeled: "AI illustration — not actual photograph"
- Never copies copyrighted images

### 8.3 Social sharing cards
- Auto-generated comparison graphics
- "I chose the Meteor 350 because..." cards for WhatsApp/Instagram
- Uses only data from our platform

### 8.4 AI ride planner
- Route planning (OpenStreetMap / Google Maps)
- Fuel stops based on your bike's tank + mileage (our data)
- Weather (OpenWeather API — free)
- Service centers (user-submitted on our platform)

### 8.5 Maintenance predictor
- Based on user-reported service logs on our platform
- "Your Meteor 350 at 10,000 km: expect chain adjustment and rear brake pad check"
- All predictions from OUR users' actual service data

---

## 9. Safety, trust & responsibility

### 9.1 Rider safety

```
RIDER SAFETY RULES (hardcoded, AI cannot override)
├── Always recommend dual-channel ABS as minimum safety feature
├── Never suggest riding above speed limits
├── Always recommend proper riding gear (helmet, gloves, jacket)
├── Flag bikes with known user-reported issues
├── Weather warnings for riding conditions
├── Emergency contacts and nearest hospital info on rides
└── Minor users: comparison only, no purchase facilitation
```

### 9.2 Data safety (DPDP Act 2023 compliant)

```
USER DATA PROTECTION
├── Consent: Explicit opt-in before collecting ANY data
├── Purpose limitation: Data used ONLY for bike recommendations
├── Data minimization: We collect only what's needed
│   ├── Height → for seat height matching (optional)
│   ├── City → for price and dealer info (optional)  
│   ├── Budget → for filtering (optional)
│   └── Email → for account only (optional, anonymous mode available)
├── Right to access: Users can download all their data
├── Right to delete: One-click delete everything
├── Right to correction: Users can edit all their data
├── Storage: Data stored in India (AWS Mumbai / GCP Mumbai)
├── Encryption: AES-256 at rest, TLS 1.3 in transit
├── No selling: We NEVER sell user data to anyone
├── No tracking: No third-party trackers, no analytics that track individuals
├── Anonymous mode: Full app usage without any account
└── Open source: Anyone can audit our data handling code
```

### 9.3 AI trust

```
TRUST PRINCIPLES
├── Every factual claim has a source citation
│   Example: "Meteor 350 weighs 191 kg [source: royalenfield.com]"
│   Example: "Average mileage 33.2 kpl [source: 1,204 user reports on RideShala]"
│
├── Confidence scores on every recommendation
│   Example: "85% confident this is the best bike for you"
│   Example: "62% confident — I need more information about your riding style"
│
├── "I don't know" when data is insufficient
│   Example: "I don't have enough service cost data for the Mavrick 440 yet 
│             (only 23 user reports). Take this estimate with caution."
│
├── No hidden sponsorships EVER
│   Our recommendations are NEVER influenced by money
│   We are open source — anyone can verify this
│
├── Transparent reasoning
│   "Why this recommendation?" button shows the full logic chain
│   Users can see exactly which data points led to the recommendation
│
└── Bias detection
    Monthly automated audit: does AI favor certain brands?
    Public bias report published quarterly
    Community can flag perceived bias via GitHub issues
```

### 9.4 Responsible AI

```
RESPONSIBLE AI CHECKLIST
├── No hallucination: RAG-only for facts, "I don't know" when unsure
├── No bias: Regular audits, no brand favoritism
├── No harmful advice: Never suggest dangerous modifications
├── No financial advice: Disclaimer on all EMI/insurance calculations
├── No gender assumptions: Gender-neutral language throughout
├── No age discrimination: Useful for 18-year-old and 50-year-old equally
├── Environmental awareness: Show emission data, suggest EVs when relevant
├── Accessibility: Screen reader compatible, high contrast mode
├── Regional inclusivity: Works for tier-2/3 cities, not just metros
└── Open source: Community can audit, improve, and fix any issues
```

---

## 10. Compliance checklist

### Laws we comply with

| Law | How we comply | Status |
|---|---|---|
| **Copyright Act 1957** | No copyrighted content used. Only OEM facts + user content | ✅ Compliant |
| **IT Act 2000 (Section 43, 66)** | No unauthorized access to any computer system, no scraping | ✅ Compliant |
| **DPDP Act 2023** | Consent-based data collection, purpose limitation, right to delete | ✅ Compliant |
| **Consumer Protection Act 2019** | No misleading recommendations, clear disclaimers | ✅ Compliant |
| **Motor Vehicles Act 1988** | No facilitation of illegal modifications | ✅ Compliant |
| **Trademarks Act 1999** | We use bike names for comparison (nominative fair use) | ✅ Compliant |
| **GDPR (if EU users)** | Same protections as DPDP, we're already compliant | ✅ Compliant |

### Using brand names and logos

**Brand names (Royal Enfield, Honda, etc.):**
- Using brand names in a comparison app is **nominative fair use** — you're identifying the product, not pretending to be the brand
- Every bike review site, automotive journalist, and comparison tool uses brand names
- This is 100% legal

**Logos:**
- We do NOT use brand logos without permission
- We use brand names in text only
- If we need visual brand identification, we use the first letter or a generic icon

### Open source license

**Our code: MIT License**
```
MIT License — free to use, modify, distribute, commercially or non-commercially.
No restrictions. Maximum freedom for the community.
```

**Our data: Creative Commons BY-SA 4.0**
```
All community-contributed specs and reviews are licensed under CC BY-SA 4.0.
Anyone can use the data with attribution. Derivative works must use same license.
This keeps the data open forever.
```

---

## 11. Tech stack (all open source / free tier)

### Everything is free or has a free tier

| Layer | Technology | License/Cost | Why |
|---|---|---|---|
| **Frontend (Web)** | Next.js 14 | MIT, free | SSR, SEO, fast |
| **Frontend (Mobile)** | Flutter | BSD, free | Cross-platform |
| **Backend API** | FastAPI (Python) | MIT, free | Async, fast, AI-native |
| **Database** | PostgreSQL | PostgreSQL License, free | Bike specs, users |
| **Vector DB** | ChromaDB or Qdrant | Apache 2.0, free | Review embeddings for RAG |
| **Cache** | Redis | BSD, free | Session, price cache |
| **Search** | Meilisearch | MIT, free | Fast fuzzy search |
| **Auth** | Supabase Auth | Apache 2.0, free tier | Social login, OTP |
| **File storage** | Supabase Storage / MinIO | Apache 2.0, free | User photos |
| **LLM** | Ollama + Llama 3.1 / Mistral | Open source, free (self-hosted) | AI responses |
| **LLM (cloud fallback)** | Claude API / Groq API | Free tier available | When self-hosted is down |
| **Embeddings** | all-MiniLM-L6-v2 / nomic-embed-text | Apache 2.0, free | Sentence embeddings |
| **Agent framework** | LangGraph / CrewAI | MIT, free | Multi-agent orchestration |
| **Maps** | OpenStreetMap + Leaflet | ODbL, free | Dealer locations |
| **Weather** | OpenWeather API | Free tier: 1,000 calls/day | Ride planning |
| **Hosting** | Vercel (frontend) + Railway/Fly.io (backend) | Free tier | Deployment |
| **CI/CD** | GitHub Actions | Free for open source | Automated testing |
| **Monitoring** | Grafana + Prometheus | Apache 2.0, free | System monitoring |

### Self-hosted LLM strategy (zero API cost)

For an open-source app, we can run AI locally:

```
PRIMARY: Ollama + Llama 3.1 8B (or Mistral 7B)
├── Runs on a single GPU server (₹2,000/month on vast.ai)
├── No per-token cost
├── Full control over the model
├── Privacy: user queries never leave our server
└── Good enough for bike recommendations

FALLBACK: Groq API (free tier)
├── 30 requests/minute free
├── Uses Llama 3.1 70B (more powerful)
└── For complex queries that need stronger reasoning

OPTIONAL: Claude API (if budget allows later)
├── Best reasoning quality
├── Pay-per-use
└── For premium tier (if we ever add one)
```

---

## 12. System architecture

```
┌─────────────┐  ┌─────────────┐  ┌──────────────┐
│ Next.js Web │  │ Flutter App │  │ Public API   │
│ (Vercel)    │  │ (iOS/And)   │  │ (for others) │
└──────┬──────┘  └──────┬──────┘  └──────┬───────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                 ┌──────▼──────┐
                 │ FastAPI     │
                 │ (Railway)   │
                 └──────┬──────┘
                        │
         ┌──────────────┼──────────────┐
         │              │              │
  ┌──────▼──────┐ ┌─────▼─────┐ ┌─────▼──────┐
  │ AI Agent    │ │ Specs API │ │ Review API │
  │ Orchestrator│ │           │ │            │
  └──────┬──────┘ └─────┬─────┘ └─────┬──────┘
         │              │              │
         │       ┌──────▼──────┐ ┌────▼──────┐
         │       │ PostgreSQL  │ │ ChromaDB  │
         │       │ (specs,     │ │ (review   │
         │       │  prices,    │ │  embed-   │
         │       │  users)     │ │  dings)   │
         │       └─────────────┘ └───────────┘
         │
  ┌──────▼──────┐
  │ Ollama /    │
  │ Llama 3.1   │
  │ (self-hosted│
  │  or Groq)   │
  └─────────────┘

  ALL DATA IS:
  ├── Community-contributed (CC BY-SA 4.0)
  ├── OEM-published facts (not copyrightable)
  ├── User-generated (with consent + license)
  ├── Government/public data
  └── Free API data (within ToS)
```

---

## 13. Data pipeline (100% legal)

```
DATA SOURCES (all legal)              PROCESSING                    STORAGE
                                       
OEM websites ──────┐                                              
(human reading +   │   ┌──────────────┐   ┌──────────────┐   ┌──────────┐
 manual entry by   ├──▶│ Validation   │──▶│ Structured   │──▶│PostgreSQL│
 contributors)     │   │ (cross-check │   │ schema       │   │          │
                   │   │  3+ sources) │   │ normalization│   └──────────┘
Govt data ─────────┤   └──────────────┘   └──────────────┘
(RTO, fuel, ins.)  │   
                   │   
Free APIs ─────────┘   
(API Ninjas, etc.)     

                       ┌──────────────┐   ┌──────────────┐   ┌──────────┐
User reviews ─────────▶│ Moderation   │──▶│ Embedding    │──▶│ ChromaDB │
(written on our app,   │ (spam check, │   │ generation   │   │ (vectors)│
 with consent)         │  quality,    │   │ (MiniLM-L6)  │   └──────────┘
                       │  toxicity)   │   └──────────────┘
User mileage logs ────▶│              │──▶ Aggregated stats ──▶ PostgreSQL
User service logs ────▶│              │──▶ Aggregated stats ──▶ PostgreSQL
User photos ──────────▶│              │──▶ Compressed ────────▶ MinIO/S3

                       CONTENT MODERATION:
                       ├── Automated: toxicity filter, spam detection
                       ├── Community: flag/report system
                       ├── Manual: volunteer moderators review flagged content
                       └── NO copyrighted content check: reject if copy-pasted
                           from other sites (plagiarism detection)
```

### Anti-plagiarism for user reviews

To prevent users from copy-pasting reviews from BikeWale/BikeDekho:

```python
def check_originality(review_text):
    """
    Reject reviews that appear to be copied from other platforms.
    Uses simple similarity check against known patterns.
    """
    # Check if review is too generic (likely copied)
    if len(review_text) < 50:
        return "too_short"
    
    # Check against common copy-paste patterns
    # (we maintain a list of known template phrases from other platforms)
    for pattern in KNOWN_COPIED_PATTERNS:
        if similarity(review_text, pattern) > 0.85:
            return "likely_copied"
    
    # Check if same text exists in our DB already
    if exact_match_in_db(review_text):
        return "duplicate"
    
    return "original"  # Accepted
```

---

## 14. MVP roadmap

### Phase 1: Foundation (Month 1-2)

- [ ] Set up PostgreSQL schema for bike specs
- [ ] Manual data entry: top 30 Indian bikes (OEM sources)
- [ ] Basic Next.js web app with comparison UI
- [ ] User registration (email or anonymous)
- [ ] User review submission with consent flow
- [ ] Basic search and filter

### Phase 2: AI layer (Month 3-4)

- [ ] Set up Ollama + Llama 3.1 (self-hosted)
- [ ] RAG pipeline: ChromaDB + user reviews
- [ ] AI chat interface ("find me a bike for...")
- [ ] AI-powered comparison with reasoning
- [ ] Source citations on every response
- [ ] Safety guardrails

### Phase 3: Community (Month 5-6)

- [ ] Mileage tracking feature (users log fill-ups)
- [ ] Service cost tracking (users log service visits)
- [ ] Community spec contributions (Wikipedia model)
- [ ] Moderation system (flag, review, approve)
- [ ] Flutter mobile app
- [ ] TCO calculator

### Phase 4: Growth (Month 7-9)

- [ ] Multi-agent system (research + analysis + safety + finance)
- [ ] AI comparison report generator
- [ ] Ride planner (OpenStreetMap + OpenWeather)
- [ ] Crowd-sourced dealer price tracker
- [ ] Multi-language support (regional Indian languages — community-driven, based on demand)
- [ ] Public API for other developers

---

## 15. Open source community strategy

### Repository structure

```
github.com/rideshala/
├── rideshala-web/          # Next.js frontend (MIT)
├── rideshala-mobile/       # Flutter app (MIT)
├── rideshala-api/          # FastAPI backend (MIT)
├── rideshala-ai/           # AI agents + RAG pipeline (MIT)
├── rideshala-data/         # Open bike database (CC BY-SA 4.0)
├── rideshala-docs/         # Documentation (CC BY 4.0)
└── .github/
    ├── CONTRIBUTING.md    # How to contribute
    ├── CODE_OF_CONDUCT.md # Community standards
    ├── LICENSE            # MIT
    └── DATA_LICENSE       # CC BY-SA 4.0
```

### How people contribute

| Contribution type | How | Reward |
|---|---|---|
| Add bike specs | Submit PR with OEM source link | Contributor badge |
| Write reviews | In-app review form | Verified reviewer badge |
| Log mileage/service | In-app tracking tools | Data contributor badge |
| Submit photos | Upload in-app (own photos only) | Photo contributor badge |
| Code contributions | GitHub PRs | Contributor credits |
| Bug reports | GitHub issues | Community karma |
| Translations | Crowdin / GitHub | Language champion badge |
| Spec verification | Cross-check existing data | Verifier badge |

### Community governance

```
GOVERNANCE MODEL (inspired by Apache Foundation)
├── Users: Anyone using the app
├── Contributors: Anyone who contributed code/data/reviews
├── Committers: Regular contributors with merge access
├── PMC (Project Management Committee): 5-7 people making decisions
└── All decisions made transparently via GitHub discussions
```

---

## 16. Cost (zero to minimal)

### Free tier hosting (MVP)

| Service | Free tier | Enough for |
|---|---|---|
| Vercel | 100GB bandwidth/month | 50,000 users |
| Railway | $5 free credit/month | Backend API |
| Supabase | 500MB DB, 1GB storage | 10,000 users |
| Groq API | 30 req/min | 1,000 AI chats/day |
| OpenWeather | 1,000 calls/day | Ride planning |
| GitHub | Unlimited for open source | Code hosting |

**Total MVP cost: ₹0/month** (within free tiers)

### When you need to scale (10,000+ users)

| Service | Cost/month |
|---|---|
| VPS for Ollama (vast.ai / RunPod) | ₹2,000–5,000 |
| Supabase Pro | ₹2,000 |
| Vercel Pro | ₹1,500 |
| Railway | ₹1,500 |
| **Total** | **₹7,000–10,000/month** |

### Funding options (to keep it free)

- **GitHub Sponsors** — community donations
- **Open Collective** — transparent funding
- **Google Summer of Code** — student contributors + Google funding
- **FOSS United India** — Indian open source grants
- **MLH Fellowship** — student contributors

---

## 17. Risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Not enough user reviews initially | AI recommendations weak | Seed with founding community of 50-100 bike owners. Gamify reviews. |
| Users copy-paste reviews from other sites | Copyright risk | Plagiarism detection. Reject obviously copied content. |
| OEM changes website structure | Manual data entry harder | Multiple contributors cross-verify. Community maintains data. |
| Self-hosted LLM quality not good enough | Poor AI responses | Use Groq free tier as fallback. Upgrade to Claude API when funded. |
| Someone forks and adds scraping | Reputation risk | MIT license allows forks. Our main repo stays clean. Can't control forks. |
| Brand sends cease-and-desist | Scary but unlikely | Nominative fair use. We're comparing products, not pretending to be them. Consult lawyer if it happens. |
| Low community participation | Slow data growth | Focus on one city (Bangalore) first. Build passionate small community before scaling. |
| Competitor with more data launches | Market risk | Our moat: open source trust + AI quality + community ownership. Data can be copied, community can't. |

---

## Summary: Why this approach wins

```
LEGALLY SAFE because:
├── Zero scraping (nothing from BikeWale/BikeDekho/ZigWheels)
├── Zero copyrighted content (only OEM facts + user content)
├── DPDP Act compliant (consent-first, minimal data, right to delete)
├── IT Act compliant (no unauthorized computer access)
├── Copyright Act compliant (facts + CC BY-SA licensed content)
└── Every data point has a documented legal source

OPEN SOURCE because:
├── MIT license (code) — anyone can use, modify, distribute
├── CC BY-SA 4.0 (data) — open motorcycle database for India
├── Transparent AI — anyone can audit our recommendation logic
├── Community-owned — not controlled by any corporation
└── No vendor lock-in — can be self-hosted by anyone

FREE because:
├── Free tier hosting covers MVP (Vercel + Railway + Supabase)
├── Self-hosted LLM (Ollama) = zero API cost
├── Open source tools throughout the stack
├── Community contributions = free labor of love
└── Funded by community donations, not ads or data selling

ZERO COMPLIANCE ISSUES because:
├── We documented every data source and its legal basis
├── We have a clear what-we-do and what-we-never-do list
├── User consent flows designed from day 1
├── Privacy-by-design architecture
├── Regular compliance audits (automated + community)
└── Open source = thousands of eyes reviewing our practices
```

---

*This is the legally bulletproof version. Build with confidence.*

*License: This document itself is released under CC BY 4.0.*

---

# PART 2: PRODUCTION UPGRADES (Claude + vLLM + LangGraph)

> **Added:** April 2026
> **Goal:** Transform the plan from a good design document into a production-ready, AI-skills-showcasing system using vLLM, Claude API, and LangGraph orchestration.

---

## 18. vLLM production LLM serving

### Why vLLM replaces Ollama

| Feature | Ollama | vLLM |
|---|---|---|
| Concurrent requests | Sequential (1 at a time) | Continuous batching (20-30+ concurrent) |
| GPU memory efficiency | Basic | PagedAttention (up to 24x better KV cache) |
| API compatibility | Custom API | OpenAI-compatible (drop-in for any OpenAI SDK client) |
| Quantization | GGUF only | AWQ, GPTQ, FP8, GGUF |
| Multi-GPU | Limited | Tensor parallelism across GPUs |
| Throughput | ~10 tokens/sec | 80-100+ tokens/sec with batching |
| Production readiness | Dev/hobbyist | Production-grade (used by major companies) |
| License | MIT | Apache 2.0 |

### Server configuration (single 24GB GPU)

```bash
# Production vLLM server launch
docker run --gpus all \
  -p 8000:8000 \
  vllm/vllm-openai:latest \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --quantization awq \
  --enable-prefix-caching \
  --gpu-memory-utilization 0.90 \
  --max-model-len 8192 \
  --api-key $VLLM_API_KEY \
  --host 0.0.0.0 \
  --port 8000
```

### GPU memory budget

| Component | Memory |
|---|---|
| Llama 3.1 8B AWQ 4-bit model weights | ~6 GB |
| nomic-embed-text FP16 (co-hosted or separate port) | ~0.5 GB |
| KV cache (managed by vLLM's PagedAttention) | ~15 GB |
| Overhead | ~2.5 GB |
| **Total** | **~24 GB** |

Supports ~20-30 concurrent inference requests with 8K context length.

### Embedding serving

```bash
# Separate vLLM instance for embeddings on port 8001
docker run --gpus all \
  -p 8001:8001 \
  vllm/vllm-openai:latest \
  --model nomic-ai/nomic-embed-text-v1.5 \
  --task embedding \
  --host 0.0.0.0 \
  --port 8001
```

### Using vLLM (OpenAI-compatible SDK)

```python
from openai import AsyncOpenAI

# vLLM uses the exact same API as OpenAI — just change the base_url
vllm_client = AsyncOpenAI(
    base_url="http://localhost:8000/v1",
    api_key=os.getenv("VLLM_API_KEY"),
)

# Chat completion (identical to OpenAI API)
response = await vllm_client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct",
    messages=[
        {"role": "system", "content": "You are RideShala, an expert motorcycle advisor..."},
        {"role": "user", "content": "Best bike for Bangalore commute under 2L?"}
    ],
    temperature=0.3,
    max_tokens=2048,
    stream=True,  # Streaming supported natively
)

# Streaming response
async for chunk in response:
    if chunk.choices[0].delta.content:
        yield chunk.choices[0].delta.content
```

### Hardware options (India-friendly pricing)

| Provider | GPU | Cost/month | Best for |
|---|---|---|---|
| vast.ai | RTX 4090 (24GB) | ₹2,000-4,000 | MVP, testing |
| RunPod | A10G (24GB) | ₹4,000-6,000 | Production |
| Lambda Cloud | A100 (40GB) | ₹8,000-12,000 | Scale (future) |
| Self-hosted | RTX 4090 | ₹0 (if you own one) | Local dev |

---

## 19. Claude API integration

### Task routing — which LLM handles what

```
USER QUERY
    │
    ▼
┌──────────────────┐
│ INTENT CLASSIFIER │ (runs on vLLM — fast, free)
└──────┬───────────┘
       │
       ├── Simple spec lookup ────────────── PostgreSQL + Meilisearch (NO LLM)
       ├── Basic chat / greetings ────────── vLLM Llama 3.1 8B (free)
       ├── Review summarization ──────────── vLLM Llama 3.1 8B (free)
       ├── Complex comparison ────────────── Claude Sonnet (premium reasoning)
       ├── Safety assessment ─────────────── Claude Sonnet (high stakes)
       ├── TCO analysis ──────────────────── Claude Sonnet (complex math + explanation)
       └── Ambiguous / unclear ───────────── Claude Sonnet (better at clarification)
```

### Fallback chain with circuit breakers

```
SIMPLE QUERIES:    vLLM (primary) ──▶ Groq free tier (fallback) ──▶ Claude (last resort)
COMPLEX QUERIES:   Claude (primary) ──▶ Groq 70B (fallback) ──▶ vLLM (degraded quality)
ALL PROVIDERS DOWN: Graceful error + cached/static response if available
```

Each provider has an independent circuit breaker:
- Opens after 5 failures in 30 seconds
- Half-open probe every 60 seconds
- When open, auto-routes to next provider

### Anthropic SDK integration

```python
import anthropic

class ClaudeProvider:
    def __init__(self):
        self.client = anthropic.AsyncAnthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    async def generate(self, messages, tools=None, system=None):
        """Generate response using Claude Sonnet."""
        response = await self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system or "You are RideShala, an expert motorcycle advisor for Indian riders...",
            messages=messages,
            tools=tools,  # For structured tool calling (comparison, TCO)
            temperature=0.3,
        )
        return response

    async def stream(self, messages, system=None):
        """Stream response using Claude Sonnet."""
        async with self.client.messages.stream(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system,
            messages=messages,
            temperature=0.3,
        ) as stream:
            async for text in stream.text_stream:
                yield text
```

### Claude tool use for structured operations

```python
# Claude can call our tools directly via Anthropic's tool_use
comparison_tools = [
    {
        "name": "search_bike_specs",
        "description": "Search motorcycle specifications database by model name",
        "input_schema": {
            "type": "object",
            "properties": {
                "model_name": {"type": "string", "description": "Bike model name, e.g., 'Meteor 350'"},
                "fields": {"type": "array", "items": {"type": "string"}, "description": "Specific fields to retrieve"}
            },
            "required": ["model_name"]
        }
    },
    {
        "name": "search_user_reviews",
        "description": "Search user reviews with semantic similarity",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "bike_model": {"type": "string"},
                "aspect": {"type": "string", "enum": ["comfort", "mileage", "performance", "build_quality", "value"]}
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate_tco",
        "description": "Calculate 5-year total cost of ownership",
        "input_schema": {
            "type": "object",
            "properties": {
                "bike_model": {"type": "string"},
                "city": {"type": "string"},
                "daily_km": {"type": "number"},
                "years": {"type": "integer", "default": 5}
            },
            "required": ["bike_model", "city", "daily_km"]
        }
    }
]
```

### Budget guardrails

```python
class CostTracker:
    """Track and enforce LLM API spending limits."""

    async def log_usage(self, provider, model, input_tokens, output_tokens, feature):
        cost = self._calculate_cost(provider, model, input_tokens, output_tokens)
        await self.db.execute(
            """INSERT INTO usage_logs
               (provider, model, input_tokens, output_tokens, feature, cost_usd, timestamp)
               VALUES ($1, $2, $3, $4, $5, $6, NOW())""",
            provider, model, input_tokens, output_tokens, feature, cost
        )

    async def check_budget(self) -> bool:
        """Returns True if daily budget still available."""
        daily_cost = await self.db.fetchval(
            "SELECT COALESCE(SUM(cost_usd), 0) FROM usage_logs WHERE timestamp > NOW() - INTERVAL '1 day'"
        )
        return daily_cost < float(os.getenv("DAILY_BUDGET_USD", "10.0"))

    async def get_provider(self, complexity: str) -> str:
        """Route to provider based on complexity and budget."""
        if not await self.check_budget():
            return "vllm"  # Budget exceeded, force free provider
        if complexity in ("comparison", "safety", "tco"):
            return "claude"
        return "vllm"
```

---

## 20. LangGraph flow orchestration

### State schema

```python
from typing import TypedDict, Annotated, Optional
from langgraph.graph import add_messages

class RideShalaState(TypedDict):
    # Conversation
    messages: Annotated[list, add_messages]
    intent: str  # bike_search, compare, safety, tco, ride_plan, general_chat, clarify

    # User context
    user_profile: Optional[dict]  # height, city, budget, riding_style
    bikes_mentioned: list[str]

    # Retrieved data (populated by agent nodes)
    specs_data: Optional[dict]
    reviews_data: Optional[list]
    mileage_data: Optional[dict]
    service_data: Optional[dict]

    # Agent outputs
    research_result: Optional[str]
    comparison_result: Optional[str]
    safety_result: Optional[str]
    finance_result: Optional[str]
    ride_plan_result: Optional[str]

    # Routing & metadata
    provider: str  # vllm, claude, groq
    needs_clarification: bool
    sources: list[str]  # Citation list
    total_tokens: int
```

### Graph definition

```python
from langgraph.graph import StateGraph, END

def build_rideshala_graph():
    graph = StateGraph(RideShalaState)

    # Add nodes
    graph.add_node("classify_intent", classify_intent_node)
    graph.add_node("clarify", clarify_node)
    graph.add_node("research", research_agent_node)
    graph.add_node("compare", comparison_agent_node)
    graph.add_node("safety_check", safety_agent_node)
    graph.add_node("finance", finance_agent_node)
    graph.add_node("ride_plan", ride_plan_agent_node)
    graph.add_node("synthesize", synthesize_node)
    graph.add_node("guardrail", guardrail_node)

    # Entry point
    graph.set_entry_point("classify_intent")

    # Conditional routing from intent classifier
    graph.add_conditional_edges(
        "classify_intent",
        route_by_intent,
        {
            "bike_search": "research",
            "compare": "compare",
            "safety": "safety_check",
            "tco": "finance",
            "ride_plan": "ride_plan",
            "general_chat": "synthesize",
            "clarify": "clarify",
        }
    )

    # All agent nodes flow to synthesize
    for node in ["research", "compare", "safety_check", "finance", "ride_plan"]:
        graph.add_edge(node, "synthesize")

    # Synthesize -> guardrail -> END
    graph.add_edge("synthesize", "guardrail")
    graph.add_edge("guardrail", END)
    graph.add_edge("clarify", END)

    return graph.compile()
```

### Agent node pattern (example: comparison agent)

```python
async def comparison_agent_node(state: RideShalaState) -> dict:
    """Compare bikes using Claude for nuanced reasoning."""
    bikes = state["bikes_mentioned"]

    # 1. RETRIEVE — get data from our legal sources
    specs = {}
    reviews = {}
    for bike in bikes:
        specs[bike] = await search_bike_specs(bike)
        reviews[bike] = await hybrid_rag_search(
            query=f"{bike} ownership experience",
            bike_model=bike,
            top_k=10
        )

    mileage = {b: await get_mileage_stats(b) for b in bikes}
    service = {b: await get_service_costs(b) for b in bikes}

    # 2. REASON — call Claude with comparison-specific prompt
    provider = await cost_tracker.get_provider("comparison")

    system_prompt = """You are RideShala's comparison agent. Compare motorcycles based on
    real data provided. For EVERY claim, cite the source. Structure your response as:
    1. Quick verdict (1 sentence)
    2. Detailed comparison by category (performance, comfort, cost, safety)
    3. Who should buy which bike (based on user profile)
    Never make claims without data backing."""

    context = format_comparison_context(specs, reviews, mileage, service, state.get("user_profile"))

    response = await llm_router.generate(
        provider=provider,
        system=system_prompt,
        messages=[{"role": "user", "content": context}],
        tools=comparison_tools,  # Claude can call tools for additional data
    )

    # 3. RETURN — update state
    return {
        "comparison_result": response.content,
        "sources": extract_citations(response),
        "total_tokens": state["total_tokens"] + response.usage.total_tokens,
    }
```

### Intent classifier

```python
async def classify_intent_node(state: RideShalaState) -> dict:
    """Fast intent classification using vLLM (free, low latency)."""
    last_message = state["messages"][-1].content

    response = await vllm_client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[{
            "role": "system",
            "content": """Classify the user's intent into exactly one category:
            - bike_search: looking for a bike recommendation
            - compare: comparing specific bikes
            - safety: asking about safety features or riding safety
            - tco: asking about costs, EMI, insurance, total ownership cost
            - ride_plan: planning a ride or route
            - general_chat: greeting, thanks, general conversation
            - clarify: message is too vague to understand what they want

            Also extract: bike names mentioned, user attributes (height, budget, city, style).
            Respond in JSON: {"intent": "...", "bikes": [...], "profile": {...}, "confidence": 0.0-1.0}"""
        }, {
            "role": "user",
            "content": last_message
        }],
        temperature=0.1,
        max_tokens=256,
        response_format={"type": "json_object"},
    )

    result = json.loads(response.choices[0].message.content)

    return {
        "intent": result["intent"] if result["confidence"] > 0.6 else "clarify",
        "bikes_mentioned": result.get("bikes", []),
        "user_profile": result.get("profile"),
        "needs_clarification": result["confidence"] <= 0.6,
        "provider": await cost_tracker.get_provider(result["intent"]),
    }
```

### Error recovery wrapper

```python
async def with_fallback(agent_fn, state, fallback_message):
    """Wrap any agent node with error recovery."""
    try:
        return await agent_fn(state)
    except ProviderUnavailableError:
        # Circuit breaker open — try next provider
        state["provider"] = get_next_provider(state["provider"])
        try:
            return await agent_fn(state)
        except Exception:
            return {"research_result": fallback_message, "sources": []}
    except RagEmptyResultError:
        return {
            "research_result": "I don't have enough data for this bike yet. "
                              "Consider contributing a review to help the community!",
            "sources": []
        }
```

---

## 21. Hybrid RAG pipeline

### Architecture (upgrade from dense-only)

```
USER QUERY: "Is Meteor 350 comfortable for long rides?"
    │
    ├──────────────────────────────────────────┐
    │                                          │
    ▼                                          ▼
┌─────────────────┐                 ┌─────────────────┐
│ DENSE SEARCH    │                 │ SPARSE SEARCH   │
│ (Qdrant)        │                 │ (Meilisearch)   │
│                 │                 │                 │
│ Embedding:      │                 │ BM25 keyword    │
│ nomic-embed-text│                 │ matching        │
│                 │                 │                 │
│ Returns: top 20 │                 │ Returns: top 20 │
│ by cosine sim   │                 │ by BM25 score   │
└────────┬────────┘                 └────────┬────────┘
         │                                   │
         └──────────────┬────────────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │ RECIPROCAL RANK │
              │ FUSION (k=60)   │
              │                 │
              │ Merges both     │
              │ result sets     │
              │ Returns: top 15 │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ CROSS-ENCODER   │
              │ RE-RANKER       │
              │                 │
              │ ms-marco-       │
              │ MiniLM-L-6-v2  │
              │ (open source)   │
              │                 │
              │ Returns: top 10 │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ CONTEXT ASSEMBLY│
              │                 │
              │ + Structured    │
              │   spec data     │
              │   (PostgreSQL)  │
              │                 │
              │ + User profile  │
              │   context       │
              │                 │
              │ + Source         │
              │   citations     │
              └────────┬────────┘
                       │
                       ▼
              LLM PROMPT (with full context + citations)
```

### Why hybrid beats dense-only

| Query type | Dense search | Sparse search | Hybrid |
|---|---|---|---|
| "Is this bike comfortable?" | Finds semantically similar reviews | Misses (no keyword "comfortable" in reviews saying "great for long rides") | Best of both |
| "Meteor 350 rear suspension stiff" | May miss exact phrasing | Finds exact keyword matches | Best of both |
| "Good bike for 5'7 rider" | Finds reviews about height/ergonomics | Misses (numbers don't match well with BM25) | Best of both |

### Implementation

```python
from qdrant_client import AsyncQdrantClient
import meilisearch

class HybridRAG:
    def __init__(self):
        self.qdrant = AsyncQdrantClient(url="http://localhost:6333")
        self.meili = meilisearch.Client("http://localhost:7700")
        self.embedder = AsyncOpenAI(base_url="http://localhost:8001/v1")  # vLLM embedding
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

    async def search(self, query: str, bike_model: str = None, top_k: int = 10):
        # 1. Parallel dense + sparse search
        dense_task = self._dense_search(query, bike_model, top_k=20)
        sparse_task = self._sparse_search(query, bike_model, top_k=20)
        dense_results, sparse_results = await asyncio.gather(dense_task, sparse_task)

        # 2. Reciprocal Rank Fusion
        fused = self._rrf_merge(dense_results, sparse_results, k=60)[:15]

        # 3. Cross-encoder re-ranking
        pairs = [(query, doc["text"]) for doc in fused]
        scores = self.reranker.predict(pairs)
        reranked = sorted(zip(fused, scores), key=lambda x: x[1], reverse=True)

        # 4. Return top_k with sources
        return [
            {
                "text": doc["text"],
                "score": float(score),
                "source": f"User review by {doc['user_id']} on RideShala ({doc['date']})",
                "bike_model": doc["bike_model"],
                "verified_owner": doc["verified_owner"],
            }
            for doc, score in reranked[:top_k]
        ]

    def _rrf_merge(self, dense, sparse, k=60):
        """Reciprocal Rank Fusion — combines two ranked lists."""
        scores = {}
        for rank, doc in enumerate(dense):
            scores[doc["id"]] = scores.get(doc["id"], 0) + 1 / (k + rank + 1)
            scores[doc["id"] + "_doc"] = doc
        for rank, doc in enumerate(sparse):
            scores[doc["id"]] = scores.get(doc["id"], 0) + 1 / (k + rank + 1)
            scores[doc["id"] + "_doc"] = doc

        ranked = sorted(
            [(id_, score) for id_, score in scores.items() if not id_.endswith("_doc")],
            key=lambda x: x[1], reverse=True
        )
        return [scores[id_ + "_doc"] for id_, _ in ranked]
```

### Batched embedding pipeline

```python
import asyncio
from redis import asyncio as aioredis

class EmbeddingPipeline:
    """Process new reviews in batches for efficiency."""

    BATCH_SIZE = 32
    FLUSH_INTERVAL = 5  # seconds

    async def run(self):
        redis = aioredis.from_url("redis://localhost:6379")
        batch = []

        while True:
            # Collect items from queue
            item = await redis.blpop("embedding_queue", timeout=self.FLUSH_INTERVAL)

            if item:
                batch.append(json.loads(item[1]))

            # Process when batch is full or timeout
            if len(batch) >= self.BATCH_SIZE or (batch and not item):
                await self._process_batch(batch)
                batch = []

    async def _process_batch(self, reviews):
        # Chunk each review by aspect (comfort, mileage, etc.)
        chunks = []
        for review in reviews:
            for aspect_chunk in self._chunk_by_aspect(review):
                chunks.append(aspect_chunk)

        # Batch embed all chunks at once
        texts = [c["text"] for c in chunks]
        embeddings = await self.embedder.embeddings.create(
            model="nomic-ai/nomic-embed-text-v1.5",
            input=texts
        )

        # Upsert to Qdrant
        points = [
            PointStruct(
                id=chunk["id"],
                vector=emb.embedding,
                payload={
                    "text": chunk["text"],
                    "bike_model": chunk["bike_model"],
                    "aspect": chunk["aspect"],
                    "user_id": chunk["user_id"],
                    "date": chunk["date"],
                    "verified_owner": chunk["verified_owner"],
                }
            )
            for chunk, emb in zip(chunks, embeddings.data)
        ]
        await self.qdrant.upsert(collection_name="user_reviews", points=points)
```

---

## 22. Production readiness

### 22.1 Rate limiting

```python
from fastapi import FastAPI, Request
from redis import asyncio as aioredis
import time

class RateLimiter:
    """Redis-backed token bucket rate limiter."""

    LIMITS = {
        "anonymous": {"chat": 10, "data": 60},    # per minute
        "authenticated": {"chat": 30, "data": 120}, # per minute
    }

    async def check(self, request: Request, endpoint_type: str) -> bool:
        user_id = request.state.user_id or request.client.host
        tier = "authenticated" if request.state.user_id else "anonymous"
        limit = self.LIMITS[tier][endpoint_type]

        key = f"rate:{user_id}:{endpoint_type}:{int(time.time()) // 60}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, 60)

        if count > limit:
            return False  # Return 429 Too Many Requests
        return True
```

### 22.2 Circuit breakers

```python
import pybreaker

# One circuit breaker per external provider
vllm_breaker = pybreaker.CircuitBreaker(
    fail_max=5,           # Open after 5 failures
    reset_timeout=60,     # Try again after 60 seconds
    name="vllm"
)

claude_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=60,
    name="claude"
)

groq_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=60,
    name="groq"
)

class LLMRouter:
    """Route to available LLM provider with automatic fallback."""

    async def generate(self, provider: str, **kwargs):
        fallback_chain = {
            "vllm": ["vllm", "groq", "claude"],
            "claude": ["claude", "groq", "vllm"],
        }

        for p in fallback_chain.get(provider, ["vllm"]):
            breaker = {"vllm": vllm_breaker, "claude": claude_breaker, "groq": groq_breaker}[p]
            try:
                return await breaker.call_async(self.providers[p].generate, **kwargs)
            except pybreaker.CircuitBreakerError:
                continue  # Circuit open, try next
            except Exception as e:
                logger.warning(f"Provider {p} failed: {e}")
                continue

        raise AllProvidersUnavailableError("All LLM providers are down")
```

### 22.3 Health checks

```python
@app.get("/health/live")
async def liveness():
    return {"status": "alive"}

@app.get("/health/ready")
async def readiness():
    checks = {
        "postgresql": await check_pg(),
        "qdrant": await check_qdrant(),
        "redis": await check_redis(),
        "llm": await check_any_llm_available(),
    }
    all_ok = all(checks.values())
    return JSONResponse(
        status_code=200 if all_ok else 503,
        content={"status": "ready" if all_ok else "not_ready", "checks": checks}
    )

@app.get("/health/startup")
async def startup_check():
    return {"status": "started", "models_loaded": True, "db_connected": True}
```

### 22.4 Observability

```python
import structlog
from opentelemetry import trace
from prometheus_client import Histogram, Counter

# Structured logging
logger = structlog.get_logger()

# Metrics
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])
LLM_TOKENS = Counter("llm_tokens_total", "Total LLM tokens", ["provider", "direction"])
ERROR_COUNT = Counter("errors_total", "Total errors", ["endpoint", "error_type"])
CACHE_HITS = Counter("cache_hits_total", "Cache hit/miss", ["cache_name", "hit"])

# Tracing
tracer = trace.get_tracer("rideshala")

# Middleware ties it all together
@app.middleware("http")
async def observability_middleware(request, call_next):
    request_id = str(uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    with tracer.start_as_current_span(f"HTTP {request.method} {request.url.path}"):
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        REQUEST_LATENCY.labels(endpoint=request.url.path).observe(duration)
        logger.info("request_completed",
            method=request.method, path=request.url.path,
            status=response.status_code, duration_ms=round(duration * 1000))

    response.headers["X-Request-ID"] = request_id
    return response
```

### 22.5 Security

```python
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
import bleach

# CORS — whitelist only our domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://rideshala.in", "http://localhost:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

# Input validation with strict limits
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    bike_models: list[str] = Field(default=[], max_length=5)

    @validator("message")
    def sanitize_message(cls, v):
        return bleach.clean(v, tags=[], strip=True)

# LLM prompt injection defense
def build_prompt(system: str, user_input: str) -> list:
    """NEVER concatenate user input into system prompt."""
    return [
        {"role": "system", "content": system},           # Our controlled prompt
        {"role": "user", "content": user_input},          # User input — separate
    ]
```

### 22.6 Deployment

```yaml
# docker-compose.yml — local development
version: "3.9"
services:
  api:
    build: ./services/api
    ports: ["8080:8080"]
    environment:
      - DATABASE_URL=postgresql://rideshala:rideshala@postgres:5432/rideshala
      - QDRANT_URL=http://qdrant:6333
      - REDIS_URL=redis://redis:6379
      - VLLM_BASE_URL=http://vllm:8000/v1
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    depends_on: [postgres, qdrant, redis, meilisearch]

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: rideshala
      POSTGRES_USER: rideshala
      POSTGRES_PASSWORD: rideshala
    volumes: ["pgdata:/var/lib/postgresql/data"]
    ports: ["5432:5432"]

  qdrant:
    image: qdrant/qdrant:latest
    volumes: ["qdrant_data:/qdrant/storage"]
    ports: ["6333:6333"]

  redis:
    image: redis:7-alpine
    ports: ["6379:6379"]

  meilisearch:
    image: getmeili/meilisearch:latest
    environment:
      MEILI_MASTER_KEY: ${MEILI_MASTER_KEY}
    volumes: ["meili_data:/meili_data"]
    ports: ["7700:7700"]

  vllm:
    image: vllm/vllm-openai:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    command: >
      --model meta-llama/Llama-3.1-8B-Instruct
      --quantization awq
      --enable-prefix-caching
      --gpu-memory-utilization 0.90
      --max-model-len 8192
    ports: ["8000:8000"]

  web:
    build: ./apps/web
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8080

volumes:
  pgdata:
  qdrant_data:
  meili_data:
```

---

## 23. Legal compliance fixes

### Fix A: Third-party model licenses

Create `THIRD_PARTY_LICENSES` in repo root:

```
THIRD-PARTY LICENSES
====================

This project uses the following third-party models and software:

1. Llama 3.1 8B Instruct
   - Provider: Meta Platforms, Inc.
   - License: Llama 3.1 Community License Agreement
   - URL: https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/LICENSE
   - Note: Free for commercial use under 700M monthly active users
   - Attribution: "Built with Meta Llama 3.1"

2. vLLM
   - License: Apache License 2.0
   - URL: https://github.com/vllm-project/vllm/blob/main/LICENSE

3. nomic-embed-text v1.5
   - Provider: Nomic AI
   - License: Apache License 2.0
   - URL: https://huggingface.co/nomic-ai/nomic-embed-text-v1.5

4. ms-marco-MiniLM-L-6-v2 (cross-encoder)
   - License: Apache License 2.0
   - URL: https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2

5. Claude API (Anthropic)
   - Usage governed by Anthropic's Terms of Service
   - URL: https://www.anthropic.com/terms
   - Note: API outputs may be used in open-source projects

6. Groq API
   - Usage governed by Groq's Terms of Service
   - Free tier: 30 requests/minute
```

### Fix B: Dual data licensing

```
DATA LICENSE
============

RideShala's community motorcycle database uses dual licensing:

1. BULK DATABASE DOWNLOADS: CC BY-SA 4.0
   Full database exports are licensed under Creative Commons
   Attribution-ShareAlike 4.0 International.
   Derivative works must use the same license.
   This keeps the open data commons alive.

2. INDIVIDUAL API RESPONSES: CC BY 4.0
   Data returned through the RideShala API is licensed under
   Creative Commons Attribution 4.0 International.
   No share-alike requirement — you can use API data in
   proprietary applications with attribution.

   Attribution format: "Data from RideShala (rideshala.in)"
```

### Fix C: Cross-border data transfer disclosure

Add to Privacy Policy:

```
CROSS-BORDER DATA TRANSFER NOTICE

When you use RideShala's AI chat features, your messages may be
processed by:

1. Self-hosted AI (vLLM): Your data stays on our servers in India
   (AWS Mumbai / GCP Mumbai). No cross-border transfer.

2. Claude AI (Anthropic): For complex analysis, your query text
   (NOT your personal data) may be sent to Anthropic's servers in
   the United States. Anthropic does not use API inputs for training.

3. Groq API: Your query text may be sent to Groq's servers in the US.

You can opt out of cross-border processing:
- Toggle "Local AI Only" in Settings
- This routes ALL queries through our self-hosted vLLM
- Quality may be slightly lower for complex comparisons
- Your data never leaves India

We comply with DPDP Act 2023 Section 16 requirements for
cross-border data transfer.
```

### Additional DPDP fixes

Add to the compliance section:

```
ADDITIONAL DPDP ACT 2023 COMPLIANCE

1. DATA FIDUCIARY REGISTRATION
   - Register with Data Protection Board of India before launch
   - Appoint Data Protection Officer (DPO) for the project
   - Maintain Records of Processing Activities (ROPA)

2. CONSENT MANAGER
   - Users can view all active consents in Settings > Privacy
   - Toggle consent per purpose: recommendations, analytics, community
   - Withdraw consent with one click (processing stops immediately)
   - Consent receipts stored in consent_logs table

3. BREACH NOTIFICATION
   - Automated monitoring for unauthorized access
   - 72-hour notification to Data Protection Board
   - Affected users notified via email and in-app alert
   - Incident response playbook documented in /docs/security/

4. DATA RETENTION
   - Chat conversations: 90 days (auto-deleted)
   - User accounts: retained until user deletes
   - Analytics: aggregated after 30 days (no individual data after that)
   - Usage logs: 1 year (for billing and abuse detection)
   - Backups: 30 days rolling

5. GRIEVANCE OFFICER
   - Name: [Project Lead Name]
   - Email: grievance@rideshala.in
   - Response time: 15 days (as required by DPDP)

6. CHILDREN'S DATA
   - Age verification at signup (self-declared, 18+)
   - Users under 18: read-only access, no data collection
   - Never use minor data for AI training or analytics
```

---

## 24. AI skills showcase

### Complete list of AI/ML skills demonstrated

```
AI SKILLS SHOWCASED IN RIDEGPT
══════════════════════════════

1.  LLM INFERENCE (vLLM)
    ├── Self-hosted Llama 3.1 8B with AWQ quantization
    ├── OpenAI-compatible API serving
    ├── Continuous batching for throughput
    ├── PagedAttention for memory efficiency
    └── Prefix caching for repeated system prompts

2.  CLOUD LLM API (Claude)
    ├── Anthropic SDK integration (AsyncAnthropic)
    ├── Tool use / function calling
    ├── Streaming responses
    ├── Token tracking and cost management
    └── Multi-model routing (Sonnet for reasoning)

3.  RAG (Retrieval-Augmented Generation)
    ├── Hybrid search (dense + sparse)
    ├── Reciprocal Rank Fusion
    ├── Cross-encoder re-ranking
    ├── Source citations on every response
    └── Context assembly with structured + unstructured data

4.  VECTOR DATABASES
    ├── Qdrant for review embeddings
    ├── Named vectors per aspect
    ├── Payload filtering (bike model, verified owner, date)
    └── Snapshot-based backups

5.  EMBEDDINGS
    ├── nomic-embed-text via vLLM serving
    ├── Batched processing pipeline (Redis queue)
    ├── Aspect-based chunking (comfort, mileage, performance)
    └── Embedding drift monitoring

6.  MULTI-AGENT SYSTEM (LangGraph)
    ├── State machine orchestration
    ├── Intent-based conditional routing
    ├── 6 specialized agents (research, comparison, safety, finance, ride, content)
    ├── Tool definitions and execution
    ├── Error recovery and fallback paths
    └── Human-in-the-loop for clarification

7.  PROMPT ENGINEERING
    ├── System prompt layering (persona + task + guardrails)
    ├── Few-shot examples per task type
    ├── Chain-of-thought reasoning for comparisons
    ├── Structured output (JSON mode)
    └── Prompt versioning as code

8.  STREAMING
    ├── Server-Sent Events (SSE) via FastAPI
    ├── vLLM native streaming
    ├── Claude streaming (messages.stream)
    └── Real-time token-by-token delivery

9.  CONTENT GENERATION
    ├── Personalized comparison reports (HTML/PDF)
    ├── Social sharing cards
    ├── AI-generated bike illustrations (Stable Diffusion)
    └── Maintenance predictions from user data

10. EVALUATION & QUALITY
    ├── RAGAS framework (faithfulness, relevancy, precision, recall)
    ├── Golden test set (200 Q&A pairs)
    ├── Automated nightly evaluation in CI
    └── Quality trend dashboards

11. FINE-TUNING (Phase 4)
    ├── QLoRA (4-bit quantization + LoRA adapters)
    ├── Hugging Face TRL + PEFT
    ├── Domain-specific motorcycle knowledge
    └── A/B testing base vs fine-tuned

12. MLOps
    ├── MLflow model versioning and tracking
    ├── A/B testing with configurable traffic splits
    ├── Model performance monitoring
    ├── Embedding distribution drift detection
    └── Public model cards

13. RESPONSIBLE AI
    ├── Hardcoded safety guardrails (always recommend ABS, gear)
    ├── Bias detection audits (brand favoritism checks)
    ├── "I don't know" when data insufficient
    ├── Confidence scores on recommendations
    ├── Transparent reasoning ("Why this recommendation?" button)
    └── No hallucination (RAG-grounded only)

14. SEARCH & RETRIEVAL
    ├── Fuzzy search (Meilisearch)
    ├── BM25 sparse retrieval
    ├── Semantic dense retrieval
    ├── Entity extraction (bike names, aspects)
    └── Query expansion (synonyms)

15. NLP
    ├── Intent classification
    ├── Sentiment analysis (review processing)
    ├── Aspect-based review chunking
    ├── Plagiarism detection (anti-copy-paste)
    ├── Toxicity filtering (content moderation)
    └── Multi-language support (regional Indian languages — community-driven)
```

---

## 25. Monorepo project structure

```
rideshala/                              (monorepo root)
│
├── apps/
│   ├── web/                          Next.js 14 frontend
│   │   ├── app/                      App router pages
│   │   │   ├── page.tsx              Home (search + chat)
│   │   │   ├── compare/page.tsx      Comparison view
│   │   │   ├── bike/[slug]/page.tsx  Individual bike page
│   │   │   ├── chat/page.tsx         AI chat interface
│   │   │   └── settings/page.tsx     Privacy, consent manager
│   │   ├── components/               Reusable UI components
│   │   ├── lib/                      API client, utils
│   │   └── package.json
│   │
│   └── mobile/                       Flutter (Phase 3+)
│       ├── lib/
│       └── pubspec.yaml
│
├── services/
│   └── api/                          FastAPI backend
│       ├── app/
│       │   ├── main.py               FastAPI app entry point
│       │   ├── api/
│       │   │   └── routes/
│       │   │       ├── chat.py       SSE streaming chat endpoint
│       │   │       ├── compare.py    Comparison endpoint
│       │   │       ├── specs.py      Bike specs CRUD
│       │   │       ├── reviews.py    Review submission + retrieval
│       │   │       ├── auth.py       Supabase auth
│       │   │       └── health.py     Health check endpoints
│       │   ├── middleware/
│       │   │   ├── rate_limiter.py
│       │   │   ├── circuit_breaker.py
│       │   │   ├── auth.py
│       │   │   └── observability.py
│       │   ├── models/               SQLAlchemy ORM models
│       │   │   ├── bike.py
│       │   │   ├── review.py
│       │   │   ├── user.py
│       │   │   └── usage_log.py
│       │   └── services/             Business logic
│       │       ├── bike_service.py
│       │       ├── review_service.py
│       │       └── consent_service.py
│       ├── alembic/                  DB migrations
│       ├── tests/
│       ├── requirements.txt
│       └── Dockerfile
│
├── packages/
│   └── ai/                           AI/ML package
│       ├── agents/
│       │   ├── graph.py              LangGraph graph definition
│       │   ├── state.py              State schema (RideShalaState)
│       │   └── nodes/
│       │       ├── classify_intent.py
│       │       ├── research.py
│       │       ├── comparison.py
│       │       ├── safety.py
│       │       ├── finance.py
│       │       ├── ride_plan.py
│       │       ├── synthesize.py
│       │       └── guardrail.py
│       ├── agents/tools/
│       │   ├── search_specs.py
│       │   ├── search_reviews.py
│       │   ├── calculators.py        EMI, RTO, insurance, TCO
│       │   ├── fuel_price.py
│       │   ├── weather.py
│       │   └── maps.py
│       ├── llm/
│       │   ├── router.py             Provider routing + fallback
│       │   ├── cost_tracker.py       Token/cost logging
│       │   └── providers/
│       │       ├── vllm_provider.py
│       │       ├── claude_provider.py
│       │       └── groq_provider.py
│       ├── rag/
│       │   ├── hybrid_search.py      Dense + sparse + RRF + reranker
│       │   ├── embeddings.py         Batched embedding pipeline
│       │   └── context_builder.py    Assemble RAG context for LLM
│       ├── evaluation/
│       │   ├── ragas_eval.py         RAGAS evaluation runner
│       │   ├── golden_testset.json   200 curated Q&A pairs
│       │   └── bias_audit.py         Brand favoritism detection
│       ├── prompts/
│       │   ├── system_base.py        Base persona prompt
│       │   ├── comparison.py         Comparison task prompt + few-shot
│       │   ├── safety.py             Safety assessment prompt
│       │   ├── finance.py            TCO/EMI prompt
│       │   └── ride_plan.py          Ride planning prompt
│       └── pyproject.toml
│
├── infra/
│   ├── docker-compose.yml            Dev environment (all services)
│   ├── docker-compose.prod.yml       Production overrides
│   ├── docker/
│   │   ├── Dockerfile.api
│   │   ├── Dockerfile.web
│   │   └── Dockerfile.vllm
│   └── k8s/                          Kubernetes (Phase 2+)
│       ├── api-deployment.yaml
│       ├── vllm-deployment.yaml
│       └── ingress.yaml
│
├── data/
│   ├── seeds/
│   │   └── bikes_india_top30.json    Initial bike data
│   └── migrations/
│       └── 001_create_qdrant_collection.py
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   ├── contributing.md
│   └── security/
│       └── incident_response.md
│
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    Lint, test, audit
│   │   ├── ragas-eval.yml            Nightly RAG evaluation
│   │   └── deploy.yml                Deploy to production
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .env.example                      Dummy values (NEVER real keys)
├── THIRD_PARTY_LICENSES              Model and library licenses
├── LICENSE                           MIT
├── DATA_LICENSE                      CC BY-SA 4.0 + CC BY 4.0 (dual)
└── README.md
```

---

## 26. Updated roadmap

### Phase 1: Foundation (Weeks 1-6)

- [ ] Initialize monorepo with apps/web, services/api, packages/ai
- [ ] PostgreSQL schema + Alembic migrations
- [ ] Seed database: top 30 Indian bikes (manual OEM data entry)
- [ ] FastAPI skeleton: health checks, rate limiter, CORS, auth middleware
- [ ] Supabase auth integration (email + anonymous)
- [ ] Next.js basic UI: search, bike page, comparison table
- [ ] Docker Compose for local dev (Postgres, Redis, Meilisearch, Qdrant)
- [ ] CI/CD pipeline (GitHub Actions: lint, test, audit)
- [ ] THIRD_PARTY_LICENSES + DATA_LICENSE files
- [ ] Privacy policy with cross-border disclosure
- [ ] DPDP consent flows (signup agreement, consent manager page)

### Phase 2: AI Layer (Weeks 7-12)

- [ ] vLLM server: AWQ-quantized Llama 3.1 8B
- [ ] vLLM embedding server: nomic-embed-text
- [ ] Qdrant collection setup + embedding pipeline (batched, Redis queue)
- [ ] Hybrid RAG: dense (Qdrant) + sparse (Meilisearch) + RRF + reranker
- [ ] LangGraph graph: intent classifier + research agent
- [ ] Claude API integration (Anthropic SDK, AsyncAnthropic)
- [ ] LLM router with fallback chain (vLLM -> Groq -> Claude)
- [ ] Circuit breakers (pybreaker, per-provider)
- [ ] Cost tracker (usage_logs table, budget guardrails)
- [ ] SSE streaming chat endpoint
- [ ] Prompt engineering: system prompts, few-shot, chain-of-thought
- [ ] RAGAS evaluation setup (50 golden test pairs)
- [ ] Observability: structlog, OpenTelemetry, Prometheus, Grafana

### Phase 3: Full Agent System (Weeks 13-18)

- [ ] Comparison agent (Claude tool use, structured output)
- [ ] Safety agent (Claude, hardcoded guardrails)
- [ ] Finance agent (TCO calculator, EMI, RTO, insurance tools)
- [ ] Review synthesis agent (vLLM, aspect-based summarization)
- [ ] User review submission with consent + moderation pipeline
- [ ] Plagiarism detection for reviews
- [ ] Mileage tracking feature (user fill-up logs)
- [ ] Service cost tracking (user service logs)
- [ ] Community spec contributions (Wikipedia model, edit review)
- [ ] Cost dashboard (Grafana: daily/monthly spend, per-feature breakdown)
- [ ] Load testing with Locust (target: 100 concurrent, p95 < 3s)
- [ ] Expand golden test set to 200 Q&A pairs

### Phase 4: Scale & Polish (Weeks 19-24)

- [ ] Flutter mobile app (iOS + Android)
- [ ] Ride planner (OpenStreetMap + OpenWeather integration)
- [ ] Crowd-sourced dealer price tracker
- [ ] QLoRA fine-tuning pipeline (after 10K+ interactions)
- [ ] A/B testing framework (base vs fine-tuned model)
- [ ] MLflow model versioning and tracking
- [ ] Multi-language support (regional Indian languages — community-driven)
- [ ] Kubernetes manifests (K3s deployment)
- [ ] Public API for other developers
- [ ] Bias audit + published model cards
- [ ] Data Fiduciary registration with DPB India

---

## Summary: Complete AI project showcase

```
WHAT THIS PROJECT DEMONSTRATES
═══════════════════════════════

AI/ML SKILLS:
├── Self-hosted LLM serving (vLLM + Llama 3.1)
├── Cloud LLM API integration (Claude Sonnet)
├── RAG pipeline (hybrid search + reranking)
├── Vector databases (Qdrant)
├── Embeddings (nomic-embed-text via vLLM)
├── Multi-agent orchestration (LangGraph)
├── Prompt engineering (versioned, few-shot, CoT)
├── Streaming responses (SSE)
├── Fine-tuning (QLoRA)
├── MLOps (MLflow, A/B testing, drift monitoring)
├── Evaluation (RAGAS)
├── NLP (intent classification, sentiment, entity extraction)
└── Responsible AI (bias audits, guardrails, citations)

ENGINEERING SKILLS:
├── Production architecture (FastAPI + Next.js + Flutter)
├── Database design (PostgreSQL + Qdrant + Redis + Meilisearch)
├── Resilience patterns (circuit breakers, rate limiting, retries)
├── Observability (structured logging, tracing, metrics, alerting)
├── Security (CORS, CSP, input validation, prompt injection defense)
├── CI/CD (GitHub Actions, automated testing, dependency scanning)
├── Containerization (Docker Compose dev, K8s prod)
├── Cost optimization (AWQ quantization, budget guardrails, tiered routing)
└── Infrastructure as code (Docker, K8s manifests)

LEGAL & COMPLIANCE:
├── 100% legal data sourcing (zero scraping)
├── DPDP Act 2023 full compliance
├── Copyright Act 1957 compliant
├── IT Act 2000 compliant
├── GDPR-ready
├── Open source licensing (MIT + CC BY-SA/CC BY dual)
├── Third-party model license compliance
├── Cross-border data transfer disclosure
└── Privacy-by-design architecture

OPEN SOURCE:
├── MIT licensed code
├── CC BY-SA open data commons
├── Community governance (Apache Foundation model)
├── Transparent AI (auditable recommendations)
├── Public bias reports
└── Anyone can self-host the entire stack
```

---

*Build plan v2 — upgraded with vLLM, Claude API, LangGraph, and production readiness.*
*Every component is free, open source, and legally compliant.*
