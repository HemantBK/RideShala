# Legal Compliance

## Golden Rule

Every data point has a documented legal source. If we can't get data legally, we don't use it.

## Data Sources (all legal)

| Data | Source | Legal basis |
|------|--------|-------------|
| Bike specifications | OEM manufacturer websites | Facts (cc, bhp, weight) are not copyrightable |
| Ex-showroom prices | Manufacturer websites + press releases | Publicly advertised commercial information |
| Bike images | OEM press/media kits | Released for editorial use |
| User reviews | Written by our own users | Explicit consent + CC BY-SA 4.0 license |
| RTO charges | parivahan.gov.in, state transport sites | Public government data |
| Insurance rates | IRDAI published tariff rates | Public regulatory data |
| Fuel prices | IOCL/BPCL official prices | Publicly published |
| Weather | Open-Meteo (open source) | Free, open API |
| Maps/routing | OpenStreetMap + OSRM | ODbL / BSD licensed |

## What We NEVER Do

- Scrape any third-party website (no competitor data)
- Copy reviews, images, or content from other platforms
- Collect personal data without explicit consent
- Use copyrighted content without permission
- Track users with third-party analytics
- Sell user data to anyone

## Indian Law Compliance

### Copyright Act 1957
Compliant — we only use factual data (not copyrightable) and user-contributed content (with license).

### IT Act 2000 (Section 43, 66)
Compliant — no unauthorized access to any computer system, no scraping.

### DPDP Act 2023

| Requirement | Implementation |
|-------------|---------------|
| Consent | Explicit opt-in before collecting any data |
| Purpose limitation | Data used only for bike recommendations |
| Data minimization | Only collect what's needed (height, city, budget — all optional) |
| Right to access | Users can download all their data |
| Right to delete | One-click delete everything |
| Right to correction | Users can edit all their data |
| Storage location | Data stored in India (AWS/GCP Mumbai) |
| Encryption | AES-256 at rest, TLS 1.3 in transit |
| Breach notification | 72-hour notification plan |
| Grievance officer | Designated with published contact |
| Children's data | Age verification, no data collection for minors |
| Data retention | Chat logs: 90 days, accounts: until deleted |

### Consumer Protection Act 2019
Compliant — no misleading recommendations, clear disclaimers on financial calculations.

### GDPR (if EU users access)
Compliant — same protections as DPDP Act.

## Cross-Border Data Transfer

When Claude API is optionally enabled, user query text (not personal data) is sent to Anthropic's US servers. Users can opt out via "Local AI Only" mode.

Default setup uses only self-hosted vLLM — no data leaves your server.

## Brand Names

Using brand names (Royal Enfield, Honda, etc.) in a comparison tool is **nominative fair use** — identifying the product, not pretending to be the brand. We do NOT use brand logos without permission.

## Licensing

| Component | License |
|-----------|---------|
| Source code | MIT — free to use, modify, distribute |
| Data (bulk download) | CC BY-SA 4.0 — derivatives must be open |
| Data (API responses) | CC BY 4.0 — use in proprietary apps with attribution |
| Third-party models | See [THIRD_PARTY_LICENSES](../THIRD_PARTY_LICENSES) |

## User Content Agreement

Users submitting reviews agree to:
1. Grant RideShala a non-exclusive license to display and distribute their content
2. License their content under CC BY-SA 4.0
3. Confirm the content is original (not copied from other platforms)
4. Confirm they can delete their content at any time

Full legal plan: [RideShala_Legal_OpenSource_Plan_v2.md](../RideShala_Legal_OpenSource_Plan_v2.md)
