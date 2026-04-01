# VaultMorph AI Shield — Task List

## PROJECT PHASES BREAKDOWN

---

## PHASE 0: Project Foundation Setup
**Goal**: Create project structure and documentation

### Task 0.1: Directory Structure ⏳
- [ ] Create app/ directory
- [ ] Create app/ui/ directory
- [ ] Create app/core/ directory
- [ ] Create app/resources/ directory
- [ ] Create config/ directory
- [ ] Create build/ directory
- [ ] Create docs/ directory

### Task 0.2: Core Documentation ⏳
- [x] Create PROJECT_GUIDE.md
- [x] Create TASKS.md
- [ ] Create progress.log
- [ ] Create README.md
- [ ] Create requirements.txt

---

## PHASE 1: Core Engine Development
**Goal**: Build detection and session management

### Task 1.1: Detection Engine 🔴
- [ ] Create detection_engine.py
- [ ] Implement rule loading from JSON
- [ ] Implement pattern matching (regex)
- [ ] Add Pro feature filtering
- [ ] Add priority-based detection
- [ ] Test with sample patterns

### Task 1.2: Rules Configuration 🔴
- [ ] Create rules.json structure
- [ ] Add basic patterns (OpenAI keys, AWS keys)
- [ ] Add JWT token pattern
- [ ] Add Pro-only patterns (private keys)
- [ ] Document rule schema
- [ ] Test rule loading

### Task 1.3: Session Manager 🔴
- [ ] Create session_manager.py
- [ ] Implement session creation (UUID)
- [ ] Implement token mapping (NAT-style)
- [ ] Implement sanitize() function
- [ ] Implement restore() function
- [ ] Add session isolation
- [ ] Test sanitize/restore cycle

---

## PHASE 2: Data Storage & Security
**Goal**: Encrypted local storage and device binding

### Task 2.1: Storage Manager 🔴
- [ ] Create storage_manager.py
- [ ] Implement Fernet encryption
- [ ] Create key generation
- [ ] Implement save() method
- [ ] Implement load() method
- [ ] Set up ~/.vaultmorph directory
- [ ] Test encryption/decryption

### Task 2.2: Device Fingerprinting 🔴
- [ ] Create device_fingerprint.py
- [ ] Implement platform detection
- [ ] Generate stable device hash
- [ ] Test across reboots
- [ ] Privacy validation (no PII)

---

## PHASE 3: Licensing System
**Goal**: Offline licensing with device binding

### Task 3.1: License Manager Core 🔴
- [ ] Create license_manager.py
- [ ] Implement local license storage
- [ ] Create signature generation
- [ ] Implement signature validation
- [ ] Add device binding
- [ ] Create is_pro() method
- [ ] Test license activation

### Task 3.2: License Schema 🔴
- [ ] Design future-proof license structure
- [ ] Add issued_by field (local/server)
- [ ] Add device_id field
- [ ] Add expiry field (nullable)
- [ ] Add type field (free/pro)
- [ ] Document license format

### Task 3.3: Backward Compatibility 🔴
- [ ] Add old license migration
- [ ] Test upgrade path
- [ ] Validate no breaking changes

---

## PHASE 4: Feature Gating
**Goal**: Clean Pro vs Free tier separation

### Task 4.1: Feature Flags 🔴
- [ ] Create feature_flags.py
- [ ] Implement max_sessions()
- [ ] Implement can_export()
- [ ] Implement can_use_advanced_detection()
- [ ] Add future-proof flag methods
- [ ] Document feature gates

---

## PHASE 5: User Interface
**Goal**: PySide6 desktop application

### Task 5.1: Main Window 🔴
- [ ] Create main_window.py
- [ ] Set up QMainWindow
- [ ] Add window title and icon
- [ ] Initialize core components
- [ ] Test window launch

### Task 5.2: Tab Management 🔴
- [ ] Implement QTabWidget
- [ ] Create new tab function
- [ ] Enforce session limits (Free: 5)
- [ ] Add tab close functionality
- [ ] Test multi-tab behavior

### Task 5.3: Input/Output Panels 🔴
- [ ] Create input QTextEdit
- [ ] Create output QTextEdit
- [ ] Add layout management
- [ ] Test text input/output

### Task 5.4: Action Buttons 🔴
- [ ] Add "Sanitize" button
- [ ] Add "Restore" button
- [ ] Connect to session manager
- [ ] Add loading states
- [ ] Test button actions

### Task 5.5: Pro Features UI 🔴
- [ ] Add "Export" button (Pro)
- [ ] Add "Import" button (Pro)
- [ ] Implement export dialog
- [ ] Implement import dialog
- [ ] Add Pro badge/indicators
- [ ] Test feature gating in UI

### Task 5.6: Update System UI 🔴
- [ ] Add "Update Rules" button
- [ ] Add "Import Rules" button
- [ ] Implement update feedback
- [ ] Add progress indicators
- [ ] Test update flow

---

## PHASE 6: Update System
**Goal**: Rules update mechanism

### Task 6.1: Update Manager 🔴
- [ ] Create update_manager.py
- [ ] Implement fetch_rules()
- [ ] Implement validate_rules()
- [ ] Implement apply_rules()
- [ ] Add URL-based updates
- [ ] Add file-based imports
- [ ] Test update safety

### Task 6.2: Configuration 🔴
- [ ] Create app_config.json
- [ ] Add server_verification flag
- [ ] Add activation_url field
- [ ] Add timeout settings
- [ ] Document config options

---

## PHASE 7: Session Export/Import
**Goal**: Pro feature for session portability

### Task 7.1: Export Functionality 🔴
- [ ] Add export_session() to session_manager
- [ ] Implement file save dialog
- [ ] Add Pro feature check
- [ ] Test export format
- [ ] Validate exported data

### Task 7.2: Import Functionality 🔴
- [ ] Add import_session() to session_manager
- [ ] Implement file open dialog
- [ ] Add validation
- [ ] Create new tab with imported data
- [ ] Test import safety

---

## PHASE 8: Application Entry Point
**Goal**: Main application launcher

### Task 8.1: Main Application 🔴
- [ ] Create app/main.py
- [ ] Initialize QApplication
- [ ] Launch MainWindow
- [ ] Add error handling
- [ ] Test application startup

---

## PHASE 9: Resources & Assets
**Goal**: Application resources

### Task 9.1: Icons & Images 🔴
- [ ] Create/add vaultmorph.ico
- [ ] Add to resources folder
- [ ] Test icon display

### Task 9.2: Rules Database 🔴
- [ ] Finalize rules.json
- [ ] Add comprehensive patterns
- [ ] Categorize by priority
- [ ] Mark Pro-only rules
- [ ] Test all patterns

---

## PHASE 10: Testing & Validation
**Goal**: Ensure stability

### Task 10.1: Unit Tests 🔴
- [ ] Test detection_engine
- [ ] Test session_manager
- [ ] Test license_manager
- [ ] Test storage_manager
- [ ] Test feature_flags

### Task 10.2: Integration Tests 🔴
- [ ] Test full sanitize/restore flow
- [ ] Test Pro feature gating
- [ ] Test license activation
- [ ] Test session limits
- [ ] Test update system

### Task 10.3: UI Tests 🔴
- [ ] Test multi-tab creation
- [ ] Test export/import
- [ ] Test button states
- [ ] Test error messages

---

## PHASE 11: Production Build
**Goal**: Distributable executable

### Task 11.1: Dependencies 🔴
- [ ] Finalize requirements.txt
- [ ] Test dependency installation
- [ ] Document Python version requirement

### Task 11.2: PyInstaller Setup 🔴
- [ ] Create build script
- [ ] Add version metadata
- [ ] Bundle resources
- [ ] Test EXE generation
- [ ] Verify EXE functionality

### Task 11.3: Version Metadata 🔴
- [ ] Create version.txt
- [ ] Add company info
- [ ] Add copyright info
- [ ] Add product description
- [ ] Test metadata embedding

---

## PHASE 12: Installer Creation
**Goal**: Professional installer

### Task 12.1: Inno Setup Script 🔴
- [ ] Create installer.iss
- [ ] Configure installation paths
- [ ] Add Start Menu shortcuts
- [ ] Add uninstaller
- [ ] Test installer

### Task 12.2: Installer Testing 🔴
- [ ] Test fresh installation
- [ ] Test upgrade path
- [ ] Test uninstallation
- [ ] Verify file cleanup

---

## PHASE 13: Documentation
**Goal**: User and developer docs

### Task 13.1: User Documentation 🔴
- [ ] Write user guide
- [ ] Create quick start guide
- [ ] Document Pro features
- [ ] Add troubleshooting section

### Task 13.2: Developer Documentation 🔴
- [ ] Document architecture
- [ ] Create API reference
- [ ] Add contribution guide
- [ ] Document build process

---

## PHASE 14: Future Enhancements (Post-MVP)
**Goal**: Advanced features

### Task 14.1: Server Activation 🟡
- [ ] Design activation API
- [ ] Implement server validation
- [ ] Add online/offline handling
- [ ] Test hybrid mode

### Task 14.2: Advanced Features 🟡
- [ ] Custom rule editor
- [ ] Pattern sharing
- [ ] Team licenses
- [ ] Usage analytics (local)

---

## STATUS LEGEND
- 🔴 Not Started
- ⏳ In Progress
- ✅ Completed
- 🟡 Future/Optional
- ❌ Blocked/Issues

---

## CURRENT PRIORITY
**Start with Phase 0 → Phase 1 → Phase 2 → Phase 3**

These are foundational and must be completed in order.
