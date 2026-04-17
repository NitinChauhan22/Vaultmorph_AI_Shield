# Changelog

All notable changes to **VaultMorph AI Shield** will be documented in this file.  
This project follows **semantic versioning**.

---

## [Unreleased]

### 🚧 Planned

- Custom rule editor (Pro)
- Clipboard watch mode (auto-sanitize on copy)
- Background tray mode
- Browser extension (Chrome/Edge integration)
- Team & enterprise audit portal
- Performance improvements for large text sessions
- Expanded rule packs (PII + API coverage)
- UI/UX refinements for session workflow

---

## [1.0.0] - 2026-04-18

### 🚀 Initial Desktop Release

**VaultMorph AI Shield v1.0.0** is the first public Windows release of the privacy layer for AI tools.

---

### ✨ Core Features

- Local **sensitive data detection engine**
- Reversible **token-based sanitization system**
- Restore original data from AI responses
- Session-based workflow (multi-tab support)
- Pop-out panels with live sync editing
- Side-by-side diff view for validation
- Rule-driven detection system (94+ patterns)

---

### 🔐 Security & Privacy

- 100% **local processing** (no data sent externally during detection)
- Encrypted local storage using **Fernet (AES-based encryption)**
- Signed rule packs verified with **Ed25519 signatures**
- Enterprise `.vml` offline license support
- No telemetry or background data collection
- Secure token mapping stored only per session

---

### 📄 Reports & Exports

- Session export to JSON
- PDF risk reports with severity breakdown
- Enterprise-grade PDF reports:
  - Executive summary
  - Risk dashboard
  - Findings table
  - Evidence samples (redacted)
  - Configuration snapshot

---

### 🧠 Detection Coverage

- API keys & tokens (AWS, OpenAI, GitHub, Stripe, etc.)
- Private keys (SSH, PGP, TLS certificates)
- Credentials (.env, Docker secrets, passwords)
- Databases (MongoDB, PostgreSQL, Redis, etc.)
- Financial identifiers (cards, IBAN, bank formats)
- PII (emails, phones, Aadhaar, PAN, UPI, SSN patterns)
- Infrastructure data (IP ranges, hostnames, internal DNS)
- Secrets manager tokens (Vault, Terraform Cloud, etc.)

---

### ⚙️ System & Architecture

- PySide6 (Qt 6) desktop UI
- Regex-based detection engine
- Token session manager with restore mapping
- Rule pack update system (signed JSON packs)
- FastAPI-based license server (enterprise backend)
- PyInstaller-based Windows packaging

---

### 📦 Licensing

- Community edition (offline, limited features)
- Pro trial (6 months, no payment required)
- Enterprise `.vml` offline license support
- Feature flags for tier-based capabilities

---

### ⚠️ Known Limitations

- Windows-only (macOS/Linux not yet supported)
- No browser extension in v1.0.0
- No real-time clipboard monitoring yet
- Rule editor not yet available
- Enterprise features require manual license provisioning

---

### 🔒 Important Notes

- VaultMorph never sends sensitive input to external servers
- Token restoration depends on session integrity
- Loss of session data may prevent full restore
- Enterprise licenses are machine-verified but offline-capable

---

## [0.9.x Beta]

### 🧪 Pre-Release Builds

- Core sanitization engine prototype
- Basic rule system (API keys + PII)
- Simple restore mechanism
- Early session UI (single-tab mode)
- Initial PDF report generator
- Prototype license system