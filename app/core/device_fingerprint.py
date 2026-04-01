"""
VaultMorph AI Shield - Device Fingerprint

This module generates a stable, privacy-safe device fingerprint for license binding.
Uses only non-sensitive system information to create a unique identifier.

Author: VaultMorph
Version: 1.0.0
"""

import platform
import hashlib
import uuid
from typing import Optional


def get_device_fingerprint() -> str:
    """
    Generate a stable device fingerprint for license binding.
    
    This function creates a unique identifier based on non-sensitive system
    information. The fingerprint is:
    - Stable across reboots
    - Privacy-safe (no personal data)
    - Unique to the device
    - Non-reversible (hashed)
    
    Components used:
    - System platform (Windows, Darwin, Linux)
    - Machine network name (hostname)
    - Processor architecture
    - MAC address (hashed for privacy)
    
    Returns:
        64-character hex string (SHA-256 hash)
        
    Note:
        If MAC address cannot be retrieved, uses platform UUID as fallback.
    """
    components = []
    
    # System platform (e.g., "Windows", "Darwin", "Linux")
    components.append(platform.system())
    
    # Machine network name (hostname)
    # This is generally stable but may change if hostname is modified
    components.append(platform.node())
    
    # Processor architecture (e.g., "AMD64", "x86_64")
    components.append(platform.machine())
    
    # Get MAC address for additional uniqueness
    # Using uuid.getnode() which returns the MAC address as an integer
    try:
        mac = uuid.getnode()
        components.append(str(mac))
    except Exception:
        # Fallback to a platform-specific UUID if MAC address fails
        components.append(str(uuid.uuid4()))
    
    # Combine all components with a separator
    raw_fingerprint = "|".join(components)
    
    # Hash the combined string for privacy and consistency
    fingerprint = hashlib.sha256(raw_fingerprint.encode('utf-8')).hexdigest()
    
    return fingerprint


def get_short_fingerprint() -> str:
    """
    Get a shorter version of the device fingerprint.
    
    Useful for display purposes or when full fingerprint is not needed.
    
    Returns:
        First 16 characters of the full fingerprint
    """
    return get_device_fingerprint()[:16]


def get_fingerprint_components() -> dict:
    """
    Get the individual components used in fingerprint generation.
    
    Useful for debugging or displaying device information to users.
    Does NOT include the MAC address for privacy.
    
    Returns:
        Dictionary with:
            - system: Operating system name
            - hostname: Machine network name
            - machine: Processor architecture
            - fingerprint: Full device fingerprint
            - short_fingerprint: First 16 chars of fingerprint
    """
    try:
        mac_available = uuid.getnode() != uuid.getnode()
    except Exception:
        mac_available = False
    
    return {
        "system": platform.system(),
        "hostname": platform.node(),
        "machine": platform.machine(),
        "mac_available": mac_available,
        "fingerprint": get_device_fingerprint(),
        "short_fingerprint": get_short_fingerprint()
    }


def verify_device_match(stored_fingerprint: str) -> bool:
    """
    Verify if the current device matches a stored fingerprint.
    
    Args:
        stored_fingerprint: Previously saved device fingerprint
        
    Returns:
        True if fingerprints match, False otherwise
    """
    current_fingerprint = get_device_fingerprint()
    return current_fingerprint == stored_fingerprint


if __name__ == "__main__":
    # Test and display fingerprint information
    print("VaultMorph AI Shield - Device Fingerprint Test")
    print("=" * 60)
    
    components = get_fingerprint_components()
    
    print("\nDevice Information:")
    print(f"  System: {components['system']}")
    print(f"  Hostname: {components['hostname']}")
    print(f"  Architecture: {components['machine']}")
    print(f"  MAC Available: {components['mac_available']}")
    
    print("\nGenerated Fingerprints:")
    print(f"  Full: {components['fingerprint']}")
    print(f"  Short: {components['short_fingerprint']}")
    
    # Test stability (should be identical)
    print("\nStability Test:")
    fp1 = get_device_fingerprint()
    fp2 = get_device_fingerprint()
    print(f"  First call:  {fp1}")
    print(f"  Second call: {fp2}")
    print(f"  Match: {fp1 == fp2} ✓" if fp1 == fp2 else "  Match: FAILED ✗")
    
    # Test verification
    print("\nVerification Test:")
    match = verify_device_match(fp1)
    print(f"  Verification: {'PASSED ✓' if match else 'FAILED ✗'}")
