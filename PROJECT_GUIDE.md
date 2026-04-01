# VaultMorph AI Shield — Project Guide

## Overview
**VaultMorph AI Shield** is a desktop (Windows-first) privacy tool that protects sensitive data before sending it to AI systems.

### Core Concept
- **Detect** sensitive data (API keys, tokens, credentials)
- **Replace** with safe tokens (sanitize)
- **Restore** original data using session-based mapping (NAT-style memory)

---

## Product Features

### Free Tier
- Sanitize + Restore (core functionality)
- Basic detection patterns
- Maximum 5 sessions
- No export capability

### Pro Tier
- Unlimited sessions
- Advanced detection patterns
- Export/import sessions
- Advanced masking options

---

## Architecture Components

### 1. UI (PySide6)
- Tab-based session interface
- Left panel: Input text
- Right panel: Sanitized output
- Session memory per tab

### 2. Detection Engine
- Pattern-based detection using rules.json
- Regex matching for sensitive data
- Priority-based detection
- Pro-only advanced patterns

### 3. Session Manager
- NAT-style token mapping
- Per-session isolation
- Sanitize and restore operations
- Export/import capability (Pro)

### 4. Storage Manager
- Encrypted local storage
- Uses cryptography.fernet
- Stores session data
- Located in user home directory

### 5. License Manager
- Offline-first licensing
- Device binding via fingerprinting
- Local signature verification
- Optional server activation (future)
- Feature flag: IS_PRO

### 6. Update Manager
- External rules.json updates
- Auto-update capability
- Manual import for offline users
- Validation before applying

---

## Licensing System

### MVP (Current)
- Format: `VM-PRO-XXXX`
- Offline validation
- Device-bound
- Local signature check

### Future Extensions
- Optional server verification
- Subscription support
- Device management
- Expiry handling

---

## Update System

Detection rules stored in external `rules.json`:
- Supports hotfix packs
- Rule updates
- Manual import (offline users)
- Validation before application

---

## Development Rules

### CRITICAL CONSTRAINTS
1. **Do NOT break existing functionality**
2. **Do NOT rewrite full files unnecessarily**
3. **Always provide minimal, modular changes**
4. **Keep backward compatibility**
5. **Test before committing**

### Code Style
- Modular functions
- Clear separation of concerns
- Type hints where applicable
- Comprehensive error handling

---

## File Structure

```
AI_Shield/
├── app/
│   ├── main.py
│   ├── ui/
│   │   └── main_window.py
│   ├── core/
│   │   ├── detection_engine.py
│   │   ├── session_manager.py
│   │   ├── storage_manager.py
│   │   ├── license_manager.py
│   │   ├── update_manager.py
│   │   ├── device_fingerprint.py
│   │   └── feature_flags.py
│   └── resources/
│       ├── vaultmorph.ico
│       └── rules.json
├── config/
│   └── app_config.json
├── build/
│   ├── version.txt
│   └── installer.iss
├── docs/
│   ├── PROJECT_GUIDE.md
│   ├── TASKS.md
│   └── progress.log
├── requirements.txt
└── README.md
```

---

## Technology Stack

- **UI Framework**: PySide6
- **Encryption**: cryptography (Fernet)
- **HTTP**: requests
- **Build**: PyInstaller
- **Installer**: Inno Setup

---

## Distribution

### Build Process
1. PyInstaller for EXE generation
2. Version metadata embedding
3. Icon integration
4. Resource bundling

### Installer
- Inno Setup script
- Start menu integration
- Uninstaller support

---

## Session Workflow

1. User creates new session (tab)
2. Enters sensitive text in input panel
3. Clicks "Sanitize"
4. Detection engine finds patterns
5. Session manager creates token mapping
6. Sanitized text appears in output
7. User can copy/use sanitized text
8. Later, paste back and click "Restore"
9. Original text recovered from mapping

---

## Privacy & Security

- **No cloud dependency** (MVP)
- **Local encryption** for storage
- **Device-bound licenses**
- **No telemetry** by default
- **User data never leaves machine**

---

## Future Roadmap

### Phase 1 (MVP) ✓
- Core sanitize/restore
- Basic UI
- Local licensing
- Free tier limits

### Phase 2
- Advanced detection patterns
- Export/import
- Rule updates
- Server activation (optional)

### Phase 3
- API integration
- Plugin system
- Custom rules editor
- Team licenses

---

## Target Users

- Developers using AI coding assistants
- Privacy-conscious professionals
- Teams with compliance requirements
- Anyone sharing sensitive data with AI

---

## Competitive Advantages

1. **Offline-first**: Works without internet
2. **Session-based**: Multiple isolated contexts
3. **Reversible**: Full data restoration
4. **Transparent**: Clear token mapping
5. **Fast**: Local processing only
