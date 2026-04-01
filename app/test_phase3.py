"""
VaultMorph AI Shield - Phase 3 Integration Test

Tests licensing system and feature gating.
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from core.license_manager import LicenseManager
from core.feature_flags import FeatureFlags, check_session_limit
from core.storage_manager import StorageManager
from core.session_manager import SessionManager
from core.detection_engine import DetectionEngine


def test_phase3():
    """Test licensing system and feature gating."""
    
    print("=" * 70)
    print("VaultMorph AI Shield - Phase 3 Integration Test")
    print("=" * 70)
    
    # Test 1: License Manager Initialization
    print("\n[1] Testing License Manager Initialization...")
    
    license_mgr = LicenseManager()
    print(f"    Storage path: {license_mgr.storage.get_storage_path()}")
    print(f"    Device ID: {license_mgr.device_id[:16]}...")
    print(f"    Initial status: {license_mgr.get_license_status()}")
    print(f"    Is Pro: {license_mgr.is_pro()}")
    
    if license_mgr.is_pro():
        print("    ✗ ERROR: Should start as Free tier!")
        return False
    print("    ✓ Starts as Free tier")
    
    # Test 2: License Key Format Validation
    print("\n[2] Testing License Key Validation...")
    
    invalid_keys = [
        "INVALID",
        "VM-FREE-12345678901234567890",
        "VM-PRO-SHORT",
        "VM-PRO-TOOLONGXXXXXXXXXXXXXXXXXX",
        ""
    ]
    
    for key in invalid_keys:
        success, msg = license_mgr.activate_license(key)
        if success:
            print(f"    ✗ ERROR: Invalid key '{key}' was accepted!")
            return False
    print("    ✓ Invalid key formats rejected")
    
    # Test 3: License Activation
    print("\n[3] Testing License Activation...")
    
    test_key = LicenseManager.generate_license_key()
    print(f"    Generated key: {test_key}")
    
    success, msg = license_mgr.activate_license(test_key)
    if not success:
        print(f"    ✗ ERROR: Activation failed: {msg}")
        return False
    print(f"    ✓ Activation successful: {msg}")
    
    # Verify Pro status
    if not license_mgr.is_pro():
        print("    ✗ ERROR: is_pro() should return True after activation!")
        return False
    print("    ✓ Pro status verified")
    
    # Test 4: License Persistence
    print("\n[4] Testing License Persistence...")
    
    # Create new manager instance (simulates app restart)
    license_mgr2 = LicenseManager()
    
    if not license_mgr2.is_pro():
        print("    ✗ ERROR: License not persisted!")
        return False
    print("    ✓ License persisted across instances")
    
    # Verify same device
    license_info = license_mgr2.get_license_info()
    if not license_info:
        print("    ✗ ERROR: No license info!")
        return False
    
    if not license_info["device_bound"]:
        print("    ✗ ERROR: Device not bound!")
        return False
    print("    ✓ Device binding working")
    
    # Test 5: Tampering Detection
    print("\n[5] Testing Tampering Detection...")
    
    # Get stored license and modify it
    stored = license_mgr2.storage.get("license")
    if not stored:
        print("    ✗ ERROR: No stored license!")
        return False
    
    original_device = stored["device_id"]
    original_signature = stored["signature"]
    
    # Tamper with device ID
    stored["device_id"] = "fake_device_12345"
    license_mgr2.storage.set("license", stored)
    
    # Reload and check
    license_mgr3 = LicenseManager()
    if license_mgr3.is_pro():
        print("    ✗ ERROR: Tampered license still valid!")
        return False
    print("    ✓ Device tampering detected")
    
    # Tamper with signature
    stored["device_id"] = original_device
    stored["signature"] = "fake_signature_123"
    license_mgr3.storage.set("license", stored)
    
    license_mgr4 = LicenseManager()
    if license_mgr4.is_pro():
        print("    ✗ ERROR: Tampered signature still valid!")
        return False
    print("    ✓ Signature tampering detected")
    
    # Restore original
    stored["signature"] = original_signature
    license_mgr4.storage.set("license", stored)
    
    # Test 6: Feature Flags - Free Tier
    print("\n[6] Testing Feature Flags - Free Tier...")
    
    # Deactivate license for free tier testing
    license_mgr.deactivate_license()
    
    free_flags = FeatureFlags(is_pro=False)
    
    # Test session limits
    if free_flags.max_sessions() != 5:
        print(f"    ✗ ERROR: Free tier should have 5 sessions, got {free_flags.max_sessions()}")
        return False
    print("    ✓ Session limit: 5")
    
    # Test session creation at limit
    if free_flags.can_create_session(5):
        print("    ✗ ERROR: Should not allow 6th session in Free tier!")
        return False
    print("    ✓ Session limit enforced")
    
    # Test export/import
    if free_flags.can_export_sessions():
        print("    ✗ ERROR: Free tier should not allow export!")
        return False
    print("    ✓ Export blocked in Free tier")
    
    if free_flags.can_import_sessions():
        print("    ✗ ERROR: Free tier should not allow import!")
        return False
    print("    ✓ Import blocked in Free tier")
    
    # Test advanced detection
    if free_flags.can_use_advanced_detection():
        print("    ✗ ERROR: Free tier should not have advanced detection!")
        return False
    print("    ✓ Advanced detection blocked")
    
    # Test 7: Feature Flags - Pro Tier
    print("\n[7] Testing Feature Flags - Pro Tier...")
    
    # Reactivate license
    success, _ = license_mgr.activate_license(test_key)
    if not success:
        print("    ✗ ERROR: Could not reactivate license!")
        return False
    
    pro_flags = FeatureFlags(is_pro=True)
    
    # Test unlimited sessions
    if pro_flags.max_sessions() != float('inf'):
        print("    ✗ ERROR: Pro tier should have unlimited sessions!")
        return False
    print("    ✓ Unlimited sessions")
    
    # Test session creation with many sessions
    if not pro_flags.can_create_session(100):
        print("    ✗ ERROR: Pro should allow 100+ sessions!")
        return False
    print("    ✓ Can create many sessions")
    
    # Test export/import
    if not pro_flags.can_export_sessions():
        print("    ✗ ERROR: Pro tier should allow export!")
        return False
    print("    ✓ Export allowed")
    
    if not pro_flags.can_import_sessions():
        print("    ✗ ERROR: Pro tier should allow import!")
        return False
    print("    ✓ Import allowed")
    
    # Test advanced detection
    if not pro_flags.can_use_advanced_detection():
        print("    ✗ ERROR: Pro tier should have advanced detection!")
        return False
    print("    ✓ Advanced detection allowed")
    
    # Test 8: Integration with Detection Engine
    print("\n[8] Testing License + Detection Engine Integration...")
    
    rules_path = app_dir / "resources" / "rules.json"
    
    # Free tier detector
    free_detector = DetectionEngine(str(rules_path), is_pro=False)
    free_stats = free_detector.get_stats()
    
    # Pro tier detector
    pro_detector = DetectionEngine(str(rules_path), is_pro=True)
    pro_stats = pro_detector.get_stats()
    
    print(f"    Free tier rules: {free_stats['free_rules']}")
    print(f"    Pro tier rules: {pro_stats['total_rules']}")
    
    if pro_stats['total_rules'] <= free_stats['free_rules']:
        print("    ✗ ERROR: Pro should have more rules than Free!")
        return False
    print("    ✓ Pro tier has additional patterns")
    
    # Test 9: Integration with Session Manager
    print("\n[9] Testing License + Session Manager Integration...")
    
    session_mgr = SessionManager()
    
    # Create 5 sessions (free limit)
    session_ids = []
    for i in range(5):
        sid = session_mgr.create_session(f"Session {i+1}")
        session_ids.append(sid)
    
    print(f"    Created {len(session_ids)} sessions")
    
    # Check with Free tier flags
    free_flags = FeatureFlags(is_pro=False)
    can_create, msg = check_session_limit(
        is_pro=False,
        current_count=session_mgr.get_session_count()
    )
    
    if can_create:
        print("    ✗ ERROR: Should not allow 6th session in Free tier!")
        return False
    print(f"    ✓ Free tier limit enforced: {msg}")
    
    # Check with Pro tier flags
    can_create, msg = check_session_limit(
        is_pro=True,
        current_count=session_mgr.get_session_count()
    )
    
    if not can_create:
        print("    ✗ ERROR: Pro tier should allow more sessions!")
        return False
    print(f"    ✓ Pro tier allows more: {msg}")
    
    # Test 10: License Information
    print("\n[10] Testing License Information...")
    
    info = license_mgr.get_license_info()
    if not info:
        print("    ✗ ERROR: No license info!")
        return False
    
    required_keys = ["type", "issued_by", "is_valid", "device_bound"]
    for key in required_keys:
        if key not in info:
            print(f"    ✗ ERROR: Missing key '{key}' in license info!")
            return False
    
    print("    License Info:")
    for key, value in info.items():
        print(f"      {key}: {value}")
    print("    ✓ License info complete")
    
    # Test 11: Feature Summary
    print("\n[11] Testing Feature Summary...")
    
    summary = pro_flags.get_feature_summary()
    
    print(f"    Tier: {summary['tier']}")
    print(f"    Max sessions: {summary['sessions']['max_sessions']}")
    print(f"    Export allowed: {summary['export_import']['can_export']}")
    print(f"    Pattern types: {len(summary['detection']['available_types'])}")
    
    if summary['tier'] != "Pro":
        print("    ✗ ERROR: Summary should show Pro tier!")
        return False
    print("    ✓ Feature summary accurate")
    
    # Cleanup
    print("\n[12] Cleanup...")
    license_mgr.deactivate_license()
    if license_mgr.is_pro():
        print("    ✗ ERROR: License not deactivated!")
        return False
    print("    ✓ License deactivated")
    
    print("\n" + "=" * 70)
    print("Phase 3 Integration Test: ✓ PASSED")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        success = test_phase3()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
