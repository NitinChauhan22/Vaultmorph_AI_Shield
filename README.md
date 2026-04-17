# VaultMorph AI Shield

**Sanitize sensitive data before it reaches AI systems. Restore it after.**

VaultMorph AI Shield is a Windows desktop application that acts as a privacy layer between you and cloud AI tools (ChatGPT, Claude, Copilot, Gemini, etc.). It detects secrets, credentials, and PII in your text, replaces them with reversible tokens before you copy to an AI, then restores the originals from the AI's response.

---

## How It Works

```
Your text with secrets  →  [Sanitize]  →  Safe tokenized text  →  AI tool
                                                                        ↓
Your text restored      ←  [Restore]   ←  AI response with tokens  ←──┘
```

No data ever leaves your machine during detection or sanitization. The AI only ever sees tokens.

---

## Tiers

| Feature | Community (Free) | Pro Trial | Enterprise |
|---|---|---|---|
| Detection rules | Community rules | All rules incl. future packs | All rules |
| Concurrent sessions | 3 | Unlimited | Unlimited |
| Session export / import | ✗ | ✓ | ✓ |
| PDF risk reports | ✓ (basic) | ✓ (full) | ✓ (enterprise) |
| Enterprise PDF report | ✗ | ✓ | ✓ |
| License type | Auto-generated offline | Server JWT (email only) | Signed .vml file |
| Internet required | Never | Activation only | Never |

**Pro Trial is free for 6 months — no credit card, no email verification.**

---

## Detection Coverage

VaultMorph AI Shield ships with a growing rule library. As of v2.0.0 the default pack covers 94+ patterns across:

- **API Keys & Tokens**: OpenAI, Anthropic, AWS (Access Key + Secret + Session Token), GitHub (classic PAT, fine-grained PAT, App tokens), GitLab, Google, Slack, Stripe, Twilio, SendGrid, Databricks, HuggingFace, npm, PyPI, DigitalOcean, Heroku, Cloudflare, Datadog, New Relic, Okta, Shopify, Square, Linear, Doppler, Pulumi, Mapbox, Terraform Cloud, Docker Hub, Firebase FCM, Postman, Supabase, PagerDuty, and more
- **Private Keys**: SSH (RSA/EC/DSA/OpenSSH), PGP, TLS certificates, GCP service account JSON
- **Credentials**: Passwords (quoted + unquoted), .env variable blocks, Docker registry credentials
- **Database Connection Strings**: MongoDB/Atlas, PostgreSQL, MySQL, Redis, MSSQL, RabbitMQ/AMQP
- **Financial**: Credit card numbers (Visa/MC/Amex/Discover), IBAN, India bank accounts
- **PII**: Email addresses, international/US/local phone numbers, India Aadhaar + PAN + UPI + IFSC + mobile, US SSN (context-anchored), UK National Insurance Number, OTP codes
- **Infrastructure**: Private IPs (RFC 1918), IPv6, public IPv4, internal hostnames (.internal/.corp/.local), Kubernetes service DNS, AWS EC2 internal DNS, Linux/Windows file paths in stack traces
- **Secrets Managers**: HashiCorp Vault tokens (hvs./hvb.), Terraform Cloud tokens

Rule packs are signed with Ed25519 and verified before import. Only VaultMorph-signed packs are accepted.

---

## Quick Start

### Install
1. Download `VaultMorphAIShield_Setup_v1.0.0.exe` from [Releases](releases/)
2. Run the installer (no admin rights needed for user install)
3. Launch **VaultMorph AI Shield** from the Start Menu or desktop shortcut

### Core workflow
1. Press **Ctrl+T** or **File → New Session** to open a session tab
2. Paste your text (with secrets, keys, PII) into **Sensitive Input**
3. Click **⬇ Sanitize** — sensitive items are replaced with `__VMX_<hex>__` tokens
4. Copy the **Sanitized Output** text and paste it into your AI tool
5. When the AI responds, paste its response back into the **Sanitized Output** box
6. Click **⬆ Restore** — tokens are swapped back to originals

### Rename a session
Double-click any session tab label to rename it. The name appears in enterprise PDF reports.

### Pop-out panels
Each panel (Sensitive Input, Sanitized Output, Side-by-Side Diff) has a **⤢ Pop-out** button. Click it to open a floating window — useful on dual monitors. Changes sync in both directions live.

---

## Licensing

### Get a free Pro Trial (recommended)
1. **License → Activate License**
2. Enter your email (identity only — not verified, no spam)
3. Click **Unlock Pro Trial — 6 months free**
4. The tier badge in the top-right updates immediately to **Pro Trial**

### Import an Enterprise license (.vml)
1. **License → Activate License**
2. Click **Import Enterprise License (.vml)…**
3. Select the `.vml` file provided by your administrator
4. Works fully offline — no server contact

### Check license status
**License → License Status** shows tier, expiry countdown, and a **Renew** button when approaching expiry. Renewal is free during the adoption phase.

---

## Rule Pack Management

### Import a signed rule pack
1. **Help → Import Rules from File…**
2. Select the `.json` file — the matching `.json.sig` must be in the same folder
3. A pre-flight dialog shows version, publisher, signature status, and before/after rule counts
4. After import the detector reloads **live** — no restart needed

### Verify the import worked
- The success dialog shows **Rules before: N → Rules now active: M**
- The status bar shows `Rules imported: vX.X.X — M rules active (+N from previous)`
- **Help → Detection Rules Reference** opens a scrollable table of every active rule — verify the count and scan for new rule names
- **Enterprise PDF report → Section 9 (Configuration Snapshot)** shows the live rule count

### Update from URL
**Help → Update Rules from URL…** — paste a URL to a signed `rules.json`. The companion `.sig` is fetched automatically from `<url>.sig`.

### Which rules file is active?
Imported packs are stored at `%APPDATA%\VaultMorph\rules.json`. This takes priority over the bundled rules on every launch — imported packs survive EXE restarts.

---

## Exports & Reports

| Export | How | Description |
|---|---|---|
| **Export JSON** | Session → Export JSON | Raw before/after text, timestamp |
| **Export PDF** | Session → Export PDF | Risk score, findings breakdown, recommendations |
| **Enterprise Report** | Session → 🔐 Enterprise Report | Full Nessus-style PDF: cover, TOC, executive summary, risk dashboard, findings table, detailed findings, evidence samples (redacted), token mapping (partial), methodology, config snapshot, recommendations, appendix |

Enterprise reports require a Sanitize to have been run first. The session name (rename by double-clicking the tab) appears as the report title.

---

## Risk Scoring

Scores are 0–100, derived from unique findings only (duplicates don't inflate the score):

| Level | Score | Examples |
|---|---|---|
| Low | 0–24 | Only phone numbers or IP addresses found |
| Medium | 25–49 | Email addresses, generic credentials |
| High | 50–74 | One AWS key, JWT token, or SSH private key |
| Critical | 75–100 | Multiple API keys or any private key |

A finding severity badge `[C] [H] [M] [L]` is shown next to each finding in the Findings panel.

---


## Support

- **Issues**: GitHub Issues
- **Email**: contact@vaultmorph.org

---

## License

**Proprietary Software** — © 2026 VaultMorph. All rights reserved.

Not for redistribution. See LICENSE file for terms.
