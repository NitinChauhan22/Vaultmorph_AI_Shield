"""
VaultMorph AI Shield - License Manager

This module handles license validation, activation, and feature gating.
Uses device binding for security and encrypted local storage for persistence.

Author: VaultMorph
Version: 1.0.0
"""

import json
import hashlib
import hmac
from typing import Optional, Dict, Any
from datetime import datetime

from .storage_manager import StorageManager
from .device_fingerprint import get_device_fingerprint


class LicenseManager:
    """
    Manages license validation and storage.
    
    Features:
    - Offline-first licensing
    - Device binding for security
    - HMAC-based signature validation
    - Encrypted license storage
    - Future-proof schema (supports server activation later)
    
    Attributes:
        storage (StorageManager): Encrypted storage instance
        device_id (str): Current device fingerprint
        license_data (Optional[Dict]): Loaded license information
    """
    
    # Secret salt for HMAC signing (in production, this should be more secure)
    # For MVP, this provides basic tamper resistance
    _SECRET_SALT = b"VaultMorph_Shield_License_Salt_v1_2026"
    
    # License key format: VM-PRO-XXXXXXXXXXXX (20 chars after prefix)
    LICENSE_KEY_PREFIX = "VM-PRO-"
    LICENSE_KEY_LENGTH = 27  # VM-PRO- (7) + 20 chars
    
    def __init__(self, storage_manager: Optional[StorageManager] = None):
        """
        Initialize license manager.
        
        Args:
            storage_manager: Optional StorageManager instance (creates new if None)
        """
        self.storage = storage_manager or StorageManager()
        self.device_id = get_device_fingerprint()
        self.license_data = self._load_license()
    
    def _generate_signature(self, license_key: str, device_id: str) -> str:
        """
        Generate HMAC signature for license validation.
        
        Args:
            license_key: The license key
            device_id: Device fingerprint
            
        Returns:
            Hex-encoded HMAC signature
        """
        # Combine key and device ID
        message = f"{license_key}|{device_id}".encode('utf-8')
        
        # Generate HMAC-SHA256 signature
        signature = hmac.new(
            self._SECRET_SALT,
            message,
            hashlib.sha256
        ).hexdigest()
        
        return signature
    
    def _validate_signature(self, license_key: str, device_id: str, signature: str) -> bool:
        """
        Validate license signature.
        
        Args:
            license_key: The license key
            device_id: Device fingerprint
            signature: Stored signature
            
        Returns:
            True if signature is valid, False otherwise
        """
        expected = self._generate_signature(license_key, device_id)
        
        # Use constant-time comparison to prevent timing attacks
        return hmac.compare_digest(expected, signature)
    
    def _validate_license_key_format(self, license_key: str) -> bool:
        """
        Validate license key format.
        
        Args:
            license_key: The license key to validate
            
        Returns:
            True if format is valid, False otherwise
        """
        if not isinstance(license_key, str):
            return False
        
        if not license_key.startswith(self.LICENSE_KEY_PREFIX):
            return False
        
        if len(license_key) != self.LICENSE_KEY_LENGTH:
            return False
        
        # Check that remaining characters are alphanumeric
        key_part = license_key[len(self.LICENSE_KEY_PREFIX):]
        return key_part.isalnum()
    
    def _load_license(self) -> Optional[Dict[str, Any]]:
        """
        Load license data from encrypted storage.
        
        Returns:
            License data dictionary or None if no license exists
        """
        license_data = self.storage.get("license")
        
        if not license_data:
            return None
        
        # Migrate old license format if needed (backward compatibility)
        if "key" in license_data and "license_key" not in license_data:
            license_data = self._migrate_old_format(license_data)
        
        return license_data
    
    def _migrate_old_format(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migrate old license format to new schema.
        
        Args:
            old_data: Old format license data
            
        Returns:
            New format license data
        """
        return {
            "license_key": old_data.get("key", ""),
            "type": "pro",
            "issued_by": "local",
            "signature": old_data.get("signature", ""),
            "device_id": old_data.get("device_id", ""),
            "expiry": None,
            "activated_at": old_data.get("activated_at")
        }
    
    def _save_license(self, license_data: Dict[str, Any]) -> bool:
        """
        Save license data to encrypted storage.
        
        Args:
            license_data: License information to save
            
        Returns:
            True if successful, False otherwise
        """
        success = self.storage.set("license", license_data)
        if success:
            self.license_data = license_data
        return success
    
    def activate_license(self, license_key: str) -> tuple[bool, str]:
        """
        Activate a license key on this device.
        
        Args:
            license_key: The license key to activate
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate key format
        if not self._validate_license_key_format(license_key):
            return False, "Invalid license key format"
        
        # Generate signature with current device
        signature = self._generate_signature(license_key, self.device_id)
        
        # Create license data
        license_data = {
            "license_key": license_key,
            "type": "pro",
            "issued_by": "local",
            "signature": signature,
            "device_id": self.device_id,
            "expiry": None,
            "activated_at": datetime.now().isoformat()
        }
        
        # Save to storage
        if self._save_license(license_data):
            return True, "License activated successfully"
        else:
            return False, "Failed to save license"
    
    def deactivate_license(self) -> bool:
        """
        Deactivate the current license.
        
        Returns:
            True if successful, False otherwise
        """
        success = self.storage.delete("license")
        if success:
            self.license_data = None
        return success
    
    def is_pro(self) -> bool:
        """
        Check if user has Pro license.
        
        This is the main method used throughout the application
        for feature gating.
        
        Returns:
            True if Pro license is active and valid, False otherwise
        """
        if not self.license_data:
            return False
        
        # Get license details
        license_key = self.license_data.get("license_key")
        stored_signature = self.license_data.get("signature")
        stored_device_id = self.license_data.get("device_id")
        issued_by = self.license_data.get("issued_by", "local")
        
        # Validate based on issuer
        if issued_by == "local":
            return self._validate_local_license(
                license_key,
                stored_device_id,
                stored_signature
            )
        elif issued_by == "server":
            # Future: server-based validation
            # For now, trust cached validation
            return self._validate_server_cached()
        
        return False
    
    def _validate_local_license(
        self,
        license_key: str,
        stored_device_id: str,
        stored_signature: str
    ) -> bool:
        """
        Validate locally-issued license.
        
        Args:
            license_key: License key
            stored_device_id: Device ID from license
            stored_signature: Signature from license
            
        Returns:
            True if valid, False otherwise
        """
        # Check key format
        if not self._validate_license_key_format(license_key):
            return False
        
        # Verify device match
        if stored_device_id != self.device_id:
            return False
        
        # Verify signature
        if not self._validate_signature(license_key, stored_device_id, stored_signature):
            return False
        
        return True
    
    def _validate_server_cached(self) -> bool:
        """
        Validate server-issued license (cached).
        
        Future implementation: This would contact server to revalidate.
        For now, we trust the cached validation.
        
        Returns:
            True (for future implementation)
        """
        # Future: implement server validation
        # For now, trust cached result
        return True
    
    def get_license_info(self) -> Optional[Dict[str, Any]]:
        """
        Get information about the current license.
        
        Returns:
            Dictionary with license information, or None if no license
        """
        if not self.license_data:
            return None
        
        return {
            "type": self.license_data.get("type", "free"),
            "issued_by": self.license_data.get("issued_by", "local"),
            "activated_at": self.license_data.get("activated_at"),
            "expiry": self.license_data.get("expiry"),
            "is_valid": self.is_pro(),
            "device_bound": self.license_data.get("device_id") == self.device_id
        }
    
    def get_license_status(self) -> str:
        """
        Get human-readable license status.
        
        Returns:
            Status string ("Pro - Active", "Free", "Pro - Invalid", etc.)
        """
        if not self.license_data:
            return "Free"
        
        if self.is_pro():
            return "Pro - Active"
        else:
            return "Pro - Invalid (Device mismatch or tampering detected)"
    
    @staticmethod
    def generate_license_key() -> str:
        """
        Generate a valid license key format.
        
        This is a helper method for testing or license generation.
        In production, keys would be generated server-side.
        
        Returns:
            Valid license key string
        """
        import secrets
        
        # Generate 20 random alphanumeric characters
        key_part = ''.join(
            secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            for _ in range(20)
        )
        
        return f"{LicenseManager.LICENSE_KEY_PREFIX}{key_part}"


if __name__ == "__main__":
    # Test license manager
    print("VaultMorph AI Shield - License Manager Test")
    print("=" * 60)
    
    # Create license manager
    print("\n[1] Initializing license manager...")
    manager = LicenseManager()
    print(f"  Storage path: {manager.storage.get_storage_path()}")
    print(f"  Device ID: {manager.device_id[:16]}...")
    
    # Check initial status
    print("\n[2] Initial license status:")
    print(f"  Status: {manager.get_license_status()}")
    print(f"  Is Pro: {manager.is_pro()}")
    
    # Generate and activate a test license
    print("\n[3] Generating test license key...")
    test_key = LicenseManager.generate_license_key()
    print(f"  Generated: {test_key}")
    
    print("\n[4] Activating license...")
    success, message = manager.activate_license(test_key)
    print(f"  Result: {message}")
    print(f"  Success: {success}")
    
    # Check status after activation
    print("\n[5] License status after activation:")
    print(f"  Status: {manager.get_license_status()}")
    print(f"  Is Pro: {manager.is_pro()}")
    
    # Get license info
    print("\n[6] License information:")
    info = manager.get_license_info()
    if info:
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    # Test tampering detection (change device ID simulation)
    print("\n[7] Testing tampering detection...")
    print("  (Simulating device ID change)")
    
    # Manually modify stored license device_id
    stored = manager.storage.get("license")
    if stored:
        original_device = stored["device_id"]
        stored["device_id"] = "fake_device_id_123"
        manager.storage.set("license", stored)
        
        # Reload and check
        manager2 = LicenseManager()
        print(f"  Is Pro after tampering: {manager2.is_pro()}")
        print(f"  Status: {manager2.get_license_status()}")
        
        # Restore original
        stored["device_id"] = original_device
        manager.storage.set("license", stored)
    
    # Test invalid key format
    print("\n[8] Testing invalid license key...")
    invalid_keys = [
        "INVALID-KEY",
        "VM-PRO-TOO-SHORT",
        "VM-FREE-XXXXXXXXXXXXXXXXXX",
        ""
    ]
    
    for invalid_key in invalid_keys:
        success, message = manager.activate_license(invalid_key)
        print(f"  Key '{invalid_key[:20]}...': {message}")
    
    # Cleanup
    print("\n[9] Cleanup...")
    manager.deactivate_license()
    print(f"  License deactivated: {manager.is_pro() == False}")
    
    print("\n" + "=" * 60)
    print("License Manager Test: ✓ COMPLETE")
