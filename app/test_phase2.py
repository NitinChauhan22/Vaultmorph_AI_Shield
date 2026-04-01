"""
VaultMorph AI Shield - Phase 2 Integration Test

Tests encrypted storage and device fingerprinting.
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from core.storage_manager import StorageManager
from core.device_fingerprint import (
    get_device_fingerprint,
    get_fingerprint_components,
    verify_device_match
)
from core.session_manager import SessionManager


def test_phase2():
    """Test storage and device fingerprinting functionality."""
    
    print("=" * 70)
    print("VaultMorph AI Shield - Phase 2 Integration Test")
    print("=" * 70)
    
    # Test 1: Device Fingerprint
    print("\n[1] Testing Device Fingerprint...")
    
    fingerprint = get_device_fingerprint()
    components = get_fingerprint_components()
    
    print(f"    Device Information:")
    print(f"      System: {components['system']}")
    print(f"      Hostname: {components['hostname']}")
    print(f"      Architecture: {components['machine']}")
    print(f"    ✓ Full fingerprint: {fingerprint}")
    print(f"    ✓ Short fingerprint: {components['short_fingerprint']}")
    
    # Test fingerprint stability
    fp2 = get_device_fingerprint()
    if fingerprint != fp2:
        print("    ✗ ERROR: Fingerprint not stable!")
        return False
    print("    ✓ Fingerprint stability verified")
    
    # Test verification
    if not verify_device_match(fingerprint):
        print("    ✗ ERROR: Device verification failed!")
        return False
    print("    ✓ Device verification working")
    
    # Test 2: Storage Manager
    print("\n[2] Testing Encrypted Storage...")
    
    storage = StorageManager(app_name="vaultmorph_test")
    print(f"    Storage path: {storage.get_storage_path()}")
    
    # Test save
    test_data = {
        "device_id": fingerprint,
        "sessions": ["session1", "session2"],
        "settings": {
            "theme": "dark",
            "auto_update": True
        }
    }
    
    if not storage.save(test_data):
        print("    ✗ ERROR: Save failed!")
        return False
    print("    ✓ Data saved successfully")
    
    # Test load
    loaded = storage.load()
    if loaded != test_data:
        print("    ✗ ERROR: Loaded data doesn't match!")
        print(f"      Original: {test_data}")
        print(f"      Loaded: {loaded}")
        return False
    print("    ✓ Data loaded successfully")
    print("    ✓ Data integrity verified")
    
    # Test encryption (verify data is actually encrypted)
    raw_data = storage.data_file.read_bytes()
    if b"device_id" in raw_data or fingerprint.encode() in raw_data:
        print("    ✗ ERROR: Data not encrypted!")
        return False
    print("    ✓ Data encryption verified")
    
    # Test get/set operations
    print("\n[3] Testing Storage Operations...")
    
    value = storage.get("device_id")
    if value != fingerprint:
        print("    ✗ ERROR: Get operation failed!")
        return False
    print("    ✓ Get operation working")
    
    if not storage.set("last_test", "2026-04-01"):
        print("    ✗ ERROR: Set operation failed!")
        return False
    
    if storage.get("last_test") != "2026-04-01":
        print("    ✗ ERROR: Set/Get mismatch!")
        return False
    print("    ✓ Set operation working")
    
    # Test exists
    if not storage.exists("device_id"):
        print("    ✗ ERROR: Exists check failed!")
        return False
    print("    ✓ Exists check working")
    
    # Test delete
    if not storage.delete("last_test"):
        print("    ✗ ERROR: Delete operation failed!")
        return False
    
    if storage.exists("last_test"):
        print("    ✗ ERROR: Key still exists after delete!")
        return False
    print("    ✓ Delete operation working")
    
    # Test 3: Storage Stats
    print("\n[4] Testing Storage Statistics...")
    
    stats = storage.get_stats()
    print(f"    Storage size: {stats['data_size_bytes']} bytes")
    print(f"    Number of keys: {stats['num_keys']}")
    print(f"    Keys: {', '.join(stats['keys'])}")
    print("    ✓ Statistics working")
    
    # Test 4: Integration with Session Manager
    print("\n[5] Testing Storage + Session Integration...")
    
    session_mgr = SessionManager()
    session_id = session_mgr.create_session("Test Session")
    
    # Export session
    session_data = session_mgr.export_session(session_id)
    
    # Save to storage
    if not storage.set(f"session_{session_id}", session_data):
        print("    ✗ ERROR: Failed to save session to storage!")
        return False
    print("    ✓ Session saved to encrypted storage")
    
    # Load from storage
    loaded_session = storage.get(f"session_{session_id}")
    if loaded_session != session_data:
        print("    ✗ ERROR: Loaded session doesn't match!")
        return False
    print("    ✓ Session loaded from storage")
    
    # Import session
    new_session_id = session_mgr.import_session(loaded_session)
    if not new_session_id:
        print("    ✗ ERROR: Failed to import session!")
        return False
    print("    ✓ Session imported successfully")
    
    # Test 5: Persistence Workflow
    print("\n[6] Testing Persistence Workflow...")
    
    # Simulate app shutdown - save all sessions
    all_sessions = {}
    for sid in [session_id, new_session_id]:
        sess_data = session_mgr.export_session(sid)
        if sess_data:
            all_sessions[sid] = sess_data
    
    storage.set("all_sessions", all_sessions)
    print(f"    ✓ Saved {len(all_sessions)} sessions to storage")
    
    # Simulate app restart - load all sessions
    new_mgr = SessionManager()
    restored_sessions = storage.get("all_sessions", {})
    
    for sid, sess_data in restored_sessions.items():
        new_mgr.import_session(sess_data)
    
    if new_mgr.get_session_count() != len(all_sessions):
        print("    ✗ ERROR: Session count mismatch after restore!")
        return False
    print("    ✓ All sessions restored successfully")
    
    # Cleanup
    print("\n[7] Cleanup...")
    storage.clear()
    if len(storage.load()) != 0:
        print("    ✗ ERROR: Storage not cleared!")
        return False
    print("    ✓ Storage cleared")
    
    print("\n" + "=" * 70)
    print("Phase 2 Integration Test: ✓ PASSED")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        success = test_phase2()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
