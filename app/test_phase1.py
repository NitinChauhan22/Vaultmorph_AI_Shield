"""
VaultMorph AI Shield - Phase 1 Integration Test

Tests the detection engine and session manager working together.
"""

import sys
from pathlib import Path

# Add app directory to path
app_dir = Path(__file__).parent
sys.path.insert(0, str(app_dir))

from core.detection_engine import DetectionEngine
from core.session_manager import SessionManager


def test_phase1():
    """Test detection and sanitization workflow."""
    
    print("=" * 70)
    print("VaultMorph AI Shield - Phase 1 Integration Test")
    print("=" * 70)
    
    # Initialize components
    print("\n[1] Initializing components...")
    rules_path = app_dir / "resources" / "rules.json"
    detector = DetectionEngine(str(rules_path), is_pro=False)
    manager = SessionManager()
    
    # Show detector stats
    stats = detector.get_stats()
    print(f"    ✓ Loaded {stats['total_rules']} detection rules")
    print(f"    ✓ Free tier: {stats['free_rules']} rules")
    print(f"    ✓ Pro tier: {stats['pro_rules']} rules (locked)")
    
    # Create session
    print("\n[2] Creating session...")
    session_id = manager.create_session("Integration Test")
    print(f"    ✓ Session created: {session_id[:8]}...")
    
    # Test text with multiple sensitive items
    test_text = """
    Development credentials for project:
    
    OpenAI API Key: sk-proj-abcd1234efgh5678ijkl9012mnop3456
    AWS Access Key: AKIAIOSFODNN7EXAMPLE
    GitHub Token: ghp_1234567890abcdefghijklmnopqrstuv
    Contact: developer@example.com
    Server IP: 192.168.1.100
    
    JWT Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
    """.strip()
    
    print("\n[3] Original text:")
    print("    " + "-" * 66)
    for line in test_text.split('\n'):
        print(f"    {line}")
    print("    " + "-" * 66)
    
    # Detect sensitive data
    print("\n[4] Running detection...")
    findings = detector.detect(test_text)
    print(f"    ✓ Found {len(findings)} sensitive items:")
    
    for i, finding in enumerate(findings, 1):
        print(f"      {i}. {finding['rule']} ({finding['type']})")
        print(f"         Match: {finding['match'][:50]}{'...' if len(finding['match']) > 50 else ''}")
        print(f"         Priority: {finding['priority']}")
    
    # Sanitize
    print("\n[5] Sanitizing text...")
    sanitized = manager.sanitize(session_id, test_text, findings)
    print("    " + "-" * 66)
    for line in sanitized.split('\n'):
        print(f"    {line}")
    print("    " + "-" * 66)
    
    # Show token mappings
    print("\n[6] Token mappings created:")
    mappings = manager.get_mapping_info(session_id)
    for mapping in mappings:
        print(f"    {mapping['token']} -> {mapping['type']} ({mapping['rule']})")
    
    # Restore
    print("\n[7] Restoring original text...")
    restored = manager.restore(session_id, sanitized)
    
    # Verify
    match = restored == test_text
    print(f"    ✓ Restoration {'successful' if match else 'FAILED'}")
    
    if not match:
        print("\n    ERROR: Restored text doesn't match original!")
        print("    Original length:", len(test_text))
        print("    Restored length:", len(restored))
        return False
    
    # Test with Pro features (should skip some patterns)
    print("\n[8] Testing Pro feature detection...")
    print("    Note: Some patterns are Pro-only and won't be detected in Free tier")
    
    pro_detector = DetectionEngine(str(rules_path), is_pro=True)
    pro_findings = pro_detector.detect(test_text)
    
    print(f"    Free tier detected: {len(findings)} items")
    print(f"    Pro tier detects: {len(pro_findings)} items")
    print(f"    Pro-only patterns: {len(pro_findings) - len(findings)} additional items")
    
    # Session stats
    print("\n[9] Session statistics:")
    session_stats = manager.get_stats()
    for key, value in session_stats.items():
        print(f"    {key}: {value}")
    
    print("\n" + "=" * 70)
    print("Phase 1 Integration Test: ✓ PASSED")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    try:
        success = test_phase1()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
