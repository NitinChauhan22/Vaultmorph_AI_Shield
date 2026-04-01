# VaultMorph AI Shield

**Privacy-First Data Protection for AI Interactions**

VaultMorph AI Shield is a desktop application that protects your sensitive data before you send it to AI systems. It detects, sanitizes, and allows you to restore your original data seamlessly.

---

## 🛡️ What It Does

VaultMorph AI Shield acts as a privacy layer between you and AI systems:

1. **Detect**: Automatically finds sensitive data (API keys, tokens, credentials)
2. **Sanitize**: Replaces sensitive data with safe tokens
3. **Restore**: Recovers your original data when needed

Think of it as a **reversible redaction tool** for the AI age.

---

## ✨ Key Features

### Free Tier
- ✅ Core sanitize & restore functionality
- ✅ Basic pattern detection (API keys, tokens)
- ✅ Up to 5 concurrent sessions
- ✅ 100% offline operation

### Pro Tier
- 🚀 Unlimited sessions
- 🚀 Advanced detection patterns
- 🚀 Export/import sessions
- 🚀 Priority support

---

## 🔒 Privacy Guaranteed

- **No cloud dependency** - Everything runs locally
- **No data collection** - Your data never leaves your machine
- **Encrypted storage** - All saved data is encrypted
- **Offline-first** - Works without internet connection

---

## 🎯 Who Is This For?

- **Developers** using AI coding assistants
- **Privacy-conscious professionals** sharing data with ChatGPT, Claude, etc.
- **Teams** with compliance requirements
- **Anyone** who values data privacy

---

## 🚀 Quick Start

### Installation

1. Download the latest installer from [Releases](releases/)
2. Run `VaultMorphInstaller.exe`
3. Launch VaultMorph AI Shield

### Usage

1. **Create a session** (click New Tab or press Ctrl+T)
2. **Paste your text** with sensitive data in the left panel
3. **Click "Sanitize"** to replace sensitive data with tokens
4. **Copy the sanitized text** from the right panel
5. **Use it safely** with any AI system
6. **To restore**: Paste the sanitized text back and click "Restore"

---

## 📋 Example

**Before (Original)**:
```
My OpenAI key is sk-proj-abc123xyz and AWS key is AKIAIOSFODNN7EXAMPLE
```

**After Sanitization**:
```
My OpenAI key is __VM_TOKEN_0__ and AWS key is __VM_TOKEN_1__
```

**After Restore**:
```
My OpenAI key is sk-proj-abc123xyz and AWS key is AKIAIOSFODNN7EXAMPLE
```

---

## 🛠️ Technology Stack

- **UI**: PySide6 (Qt6)
- **Encryption**: Fernet (cryptography library)
- **Detection**: Regex-based pattern matching
- **Platform**: Windows (macOS/Linux support planned)

---

## 📦 Building from Source

### Prerequisites
- Python 3.9 or higher
- pip

### Steps

```bash
# Clone or download the repository
cd AI_Shield

# Install dependencies
pip install -r requirements.txt

# Run the application
python app/main.py

# Build executable
pyinstaller app/main.py --version-file=build/version.txt
```

---

## 🗺️ Roadmap

### ✅ MVP (Current)
- Core sanitize/restore functionality
- Basic UI with session tabs
- Free and Pro tiers
- Offline licensing

### 🔜 Phase 2
- Advanced detection patterns
- Custom rule editor
- Auto-update system
- Server activation option

### 🔮 Future
- Browser extension
- API integration
- Team licenses
- Plugin system

---

## 📁 Project Structure

```
AI_Shield/
├── app/
│   ├── main.py              # Application entry point
│   ├── ui/
│   │   └── main_window.py   # Main UI window
│   ├── core/
│   │   ├── detection_engine.py    # Pattern detection
│   │   ├── session_manager.py     # Session handling
│   │   ├── storage_manager.py     # Encrypted storage
│   │   ├── license_manager.py     # License validation
│   │   ├── update_manager.py      # Rule updates
│   │   ├── device_fingerprint.py  # Device binding
│   │   └── feature_flags.py       # Feature gating
│   └── resources/
│       ├── vaultmorph.ico
│       └── rules.json       # Detection patterns
├── config/
│   └── app_config.json      # Application config
├── build/
│   ├── version.txt          # EXE metadata
│   └── installer.iss        # Inno Setup script
├── docs/
│   ├── PROJECT_GUIDE.md     # Master context
│   ├── TASKS.md             # Development tasks
│   └── progress.log         # Progress tracking
├── requirements.txt
└── README.md
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Development Guide](docs/PROJECT_GUIDE.md) for details.

### For Developers
- Read [PROJECT_GUIDE.md](docs/PROJECT_GUIDE.md) for architecture overview
- Check [TASKS.md](docs/TASKS.md) for current development phases
- See [progress.log](docs/progress.log) for what's been completed

---

## 📄 License

**Proprietary Software**  
© 2026 VaultMorph. All rights reserved.

---

## 💬 Support

- **Documentation**: [docs/](docs/)
- **Issues**: GitHub Issues (coming soon)
- **Email**: support@vaultmorph.com (coming soon)

---

## ⚠️ Important Notes

- VaultMorph AI Shield is in **active development**
- This is a **privacy tool**, not a security tool
- Always review sanitized output before sharing
- Token mappings are session-specific

---

## 🙏 Acknowledgments

Built with the goal of making AI interactions safer and more private for everyone.

**Made with ❤️ for privacy-conscious users**
