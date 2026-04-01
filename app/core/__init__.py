"""
VaultMorph AI Shield - Core Module

This package contains the core functionality of VaultMorph AI Shield.

Modules:
    - detection_engine: Pattern-based detection of sensitive data
    - session_manager: Session management and NAT-style token mapping
    - storage_manager: Encrypted local storage
    - device_fingerprint: Device identification for license binding
    - license_manager: License validation and feature gating
    - feature_flags: Feature gating logic (Free vs Pro)
    - update_manager: Rules update system (coming soon)
"""

__version__ = "1.0.0"
__author__ = "VaultMorph"

from .detection_engine import DetectionEngine, create_detector
from .session_manager import SessionManager
from .storage_manager import StorageManager
from .device_fingerprint import (
    get_device_fingerprint,
    get_short_fingerprint,
    get_fingerprint_components,
    verify_device_match
)
from .license_manager import LicenseManager
from .feature_flags import (
    FeatureFlags,
    check_session_limit,
    check_export_permission,
    check_import_permission
)

__all__ = [
    "DetectionEngine",
    "create_detector",
    "SessionManager",
    "StorageManager",
    "get_device_fingerprint",
    "get_short_fingerprint",
    "get_fingerprint_components",
    "verify_device_match",
    "LicenseManager",
    "FeatureFlags",
    "check_session_limit",
    "check_export_permission",
    "check_import_permission",
]
