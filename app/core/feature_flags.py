"""
VaultMorph AI Shield - Feature Flags

Centralized feature gating logic for Free vs Pro tiers.
This module provides a clean interface for checking feature availability
throughout the application.

Author: VaultMorph
Version: 1.0.0
"""

from typing import Dict, Any, List


class FeatureFlags:
    """
    Centralized feature gating for Free vs Pro tiers.
    
    This class encapsulates all feature availability logic,
    making it easy to manage tier differences and add new features.
    
    Attributes:
        is_pro (bool): Whether the user has Pro license
    """
    
    def __init__(self, is_pro: bool):
        """
        Initialize feature flags.
        
        Args:
            is_pro: Whether user has active Pro license
        """
        self.is_pro = is_pro
    
    # ==================== Session Features ====================
    
    def max_sessions(self) -> int:
        """
        Get maximum number of concurrent sessions allowed.
        
        Returns:
            Maximum sessions (5 for Free, unlimited for Pro)
        """
        return float('inf') if self.is_pro else 5
    
    def can_create_session(self, current_count: int) -> bool:
        """
        Check if user can create a new session.
        
        Args:
            current_count: Current number of sessions
            
        Returns:
            True if new session can be created, False otherwise
        """
        max_allowed = self.max_sessions()
        
        if max_allowed == float('inf'):
            return True
        
        return current_count < max_allowed
    
    # ==================== Export/Import Features ====================
    
    def can_export_sessions(self) -> bool:
        """
        Check if user can export sessions.
        
        Returns:
            True if export is allowed (Pro only)
        """
        return self.is_pro
    
    def can_import_sessions(self) -> bool:
        """
        Check if user can import sessions.
        
        Returns:
            True if import is allowed (Pro only)
        """
        return self.is_pro
    
    # ==================== Detection Features ====================
    
    def can_use_advanced_detection(self) -> bool:
        """
        Check if user can use advanced detection patterns.
        
        Returns:
            True if advanced patterns are allowed (Pro only)
        """
        return self.is_pro
    
    def get_available_pattern_types(self) -> List[str]:
        """
        Get list of available pattern types for current tier.
        
        Returns:
            List of pattern type names
        """
        if self.is_pro:
            return [
                "api_key",
                "token",
                "pii",
                "network",
                "private_key",  # Pro only
                "credential",    # Pro only
                "financial"      # Pro only
            ]
        else:
            return [
                "api_key",
                "token",
                "pii",
                "network"
            ]
    
    # ==================== Storage Features ====================
    
    def can_use_backup(self) -> bool:
        """
        Check if user can use backup/restore features.
        
        Returns:
            True if backup is allowed (Pro only)
        """
        return self.is_pro
    
    def max_storage_size_mb(self) -> int:
        """
        Get maximum storage size allowed.
        
        Returns:
            Maximum storage in MB (10 for Free, 100 for Pro)
        """
        return 100 if self.is_pro else 10
    
    # ==================== Update Features ====================
    
    def can_auto_update_rules(self) -> bool:
        """
        Check if automatic rule updates are allowed.
        
        Returns:
            True if auto-update is allowed (Pro feature, but free gets it too)
        """
        # Auto-updates are available to all tiers for security
        return True
    
    def can_import_custom_rules(self) -> bool:
        """
        Check if user can import custom detection rules.
        
        Returns:
            True if custom rules allowed (Pro only)
        """
        return self.is_pro
    
    # ==================== UI Features ====================
    
    def can_customize_theme(self) -> bool:
        """
        Check if user can customize UI theme.
        
        Returns:
            True if theme customization allowed (Pro only)
        """
        return self.is_pro
    
    def show_pro_badge(self) -> bool:
        """
        Check if Pro badge should be shown in UI.
        
        Returns:
            True if user has Pro license
        """
        return self.is_pro
    
    # ==================== Advanced Features (Future) ====================
    
    def can_use_api(self) -> bool:
        """
        Check if user can use API features (future).
        
        Returns:
            True if API access allowed (Pro only)
        """
        return self.is_pro
    
    def can_use_team_features(self) -> bool:
        """
        Check if user can use team collaboration (future).
        
        Returns:
            True if team features allowed (Enterprise only, future)
        """
        # Future: check for enterprise license
        return False
    
    # ==================== Feature Summary ====================
    
    def get_feature_summary(self) -> Dict[str, Any]:
        """
        Get summary of all feature flags.
        
        Useful for debugging and displaying to users.
        
        Returns:
            Dictionary with all feature flags and their values
        """
        return {
            "tier": "Pro" if self.is_pro else "Free",
            "sessions": {
                "max_sessions": self.max_sessions() if self.max_sessions() != float('inf') else "Unlimited",
            },
            "export_import": {
                "can_export": self.can_export_sessions(),
                "can_import": self.can_import_sessions(),
            },
            "detection": {
                "advanced_patterns": self.can_use_advanced_detection(),
                "available_types": self.get_available_pattern_types(),
            },
            "storage": {
                "backup_restore": self.can_use_backup(),
                "max_size_mb": self.max_storage_size_mb(),
            },
            "updates": {
                "auto_update": self.can_auto_update_rules(),
                "custom_rules": self.can_import_custom_rules(),
            },
            "ui": {
                "theme_customization": self.can_customize_theme(),
                "pro_badge": self.show_pro_badge(),
            },
            "future": {
                "api_access": self.can_use_api(),
                "team_features": self.can_use_team_features(),
            }
        }
    
    def get_upgrade_benefits(self) -> List[str]:
        """
        Get list of benefits for upgrading to Pro.
        
        Returns:
            List of Pro features not available in Free tier
        """
        if self.is_pro:
            return []
        
        return [
            "Unlimited sessions (vs. 5 in Free)",
            "Export and import sessions",
            "Advanced detection patterns (private keys, credentials, financial data)",
            "Backup and restore functionality",
            "Import custom detection rules",
            "UI theme customization",
            "API access (future)",
            "Priority support",
        ]
    
    def get_tier_name(self) -> str:
        """
        Get the current tier name.
        
        Returns:
            "Pro" or "Free"
        """
        return "Pro" if self.is_pro else "Free"


# Convenience functions for common checks

def check_session_limit(is_pro: bool, current_count: int) -> tuple[bool, str]:
    """
    Check if a new session can be created.
    
    Args:
        is_pro: Whether user has Pro license
        current_count: Current number of sessions
        
    Returns:
        Tuple of (can_create: bool, message: str)
    """
    flags = FeatureFlags(is_pro)
    
    if flags.can_create_session(current_count):
        return True, "OK"
    else:
        max_sessions = flags.max_sessions()
        return False, f"Free tier limited to {int(max_sessions)} sessions. Upgrade to Pro for unlimited sessions."


def check_export_permission(is_pro: bool) -> tuple[bool, str]:
    """
    Check if export is allowed.
    
    Args:
        is_pro: Whether user has Pro license
        
    Returns:
        Tuple of (can_export: bool, message: str)
    """
    flags = FeatureFlags(is_pro)
    
    if flags.can_export_sessions():
        return True, "OK"
    else:
        return False, "Export feature requires Pro license."


def check_import_permission(is_pro: bool) -> tuple[bool, str]:
    """
    Check if import is allowed.
    
    Args:
        is_pro: Whether user has Pro license
        
    Returns:
        Tuple of (can_import: bool, message: str)
    """
    flags = FeatureFlags(is_pro)
    
    if flags.can_import_sessions():
        return True, "OK"
    else:
        return False, "Import feature requires Pro license."


if __name__ == "__main__":
    # Test feature flags
    print("VaultMorph AI Shield - Feature Flags Test")
    print("=" * 60)
    
    # Test Free tier
    print("\n[1] Free Tier Features:")
    free_flags = FeatureFlags(is_pro=False)
    free_summary = free_flags.get_feature_summary()
    
    print(f"  Tier: {free_summary['tier']}")
    print(f"  Max sessions: {free_summary['sessions']['max_sessions']}")
    print(f"  Can export: {free_summary['export_import']['can_export']}")
    print(f"  Can import: {free_summary['export_import']['can_import']}")
    print(f"  Advanced detection: {free_summary['detection']['advanced_patterns']}")
    print(f"  Pattern types: {', '.join(free_summary['detection']['available_types'])}")
    
    # Test Pro tier
    print("\n[2] Pro Tier Features:")
    pro_flags = FeatureFlags(is_pro=True)
    pro_summary = pro_flags.get_feature_summary()
    
    print(f"  Tier: {pro_summary['tier']}")
    print(f"  Max sessions: {pro_summary['sessions']['max_sessions']}")
    print(f"  Can export: {pro_summary['export_import']['can_export']}")
    print(f"  Can import: {pro_summary['export_import']['can_import']}")
    print(f"  Advanced detection: {pro_summary['detection']['advanced_patterns']}")
    print(f"  Pattern types: {', '.join(pro_summary['detection']['available_types'])}")
    
    # Test session limits
    print("\n[3] Session Limit Tests:")
    
    # Free tier - within limit
    can_create, msg = check_session_limit(is_pro=False, current_count=3)
    print(f"  Free tier, 3 sessions: {can_create} - {msg}")
    
    # Free tier - at limit
    can_create, msg = check_session_limit(is_pro=False, current_count=5)
    print(f"  Free tier, 5 sessions: {can_create} - {msg}")
    
    # Pro tier - many sessions
    can_create, msg = check_session_limit(is_pro=True, current_count=100)
    print(f"  Pro tier, 100 sessions: {can_create} - {msg}")
    
    # Test export/import
    print("\n[4] Export/Import Permission Tests:")
    
    can_export, msg = check_export_permission(is_pro=False)
    print(f"  Free tier export: {can_export} - {msg}")
    
    can_export, msg = check_export_permission(is_pro=True)
    print(f"  Pro tier export: {can_export} - {msg}")
    
    # Show upgrade benefits
    print("\n[5] Upgrade Benefits (Free -> Pro):")
    benefits = free_flags.get_upgrade_benefits()
    for i, benefit in enumerate(benefits, 1):
        print(f"  {i}. {benefit}")
    
    print("\n" + "=" * 60)
    print("Feature Flags Test: ✓ COMPLETE")
