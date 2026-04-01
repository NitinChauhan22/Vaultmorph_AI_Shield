"""
VaultMorph AI Shield - Detection Engine

This module handles the detection of sensitive data patterns using regex-based rules.
Rules are loaded from an external JSON file and can be updated dynamically.

Author: VaultMorph
Version: 1.0.0
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional


class DetectionEngine:
    """
    Core detection engine for identifying sensitive data patterns.
    
    Attributes:
        rules_path (Path): Path to the rules.json file
        is_pro (bool): Whether Pro features are enabled
        rules (List[Dict]): Loaded detection rules
    """
    
    def __init__(self, rules_path: str, is_pro: bool = False):
        """
        Initialize the detection engine.
        
        Args:
            rules_path: Path to the rules.json file
            is_pro: Whether the user has Pro license (enables advanced patterns)
        """
        self.rules_path = Path(rules_path)
        self.is_pro = is_pro
        self.rules = self.load_rules()
    
    def load_rules(self) -> List[Dict[str, Any]]:
        """
        Load detection rules from the JSON file.
        
        Returns:
            List of rule dictionaries
            
        Raises:
            FileNotFoundError: If rules file doesn't exist
            json.JSONDecodeError: If rules file is invalid JSON
        """
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            rules = data.get("patterns", [])
            
            # Sort rules by priority (lower number = higher priority)
            rules.sort(key=lambda x: x.get("priority", 999))
            
            return rules
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Rules file not found: {self.rules_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in rules file: {e}")
    
    def reload_rules(self) -> bool:
        """
        Reload rules from the JSON file.
        Useful after rules have been updated.
        
        Returns:
            True if reload successful, False otherwise
        """
        try:
            self.rules = self.load_rules()
            return True
        except Exception:
            return False
    
    def detect(self, text: str) -> List[Dict[str, Any]]:
        """
        Detect sensitive data in the provided text.
        
        Args:
            text: The text to scan for sensitive data
            
        Returns:
            List of findings, each containing:
                - type: The type of sensitive data
                - match: The matched text
                - rule: The name of the rule that matched
                - start: Start position in text
                - end: End position in text
                - priority: Rule priority (0 = highest)
        """
        findings = []
        
        for rule in self.rules:
            # Skip Pro-only rules if user doesn't have Pro license
            if rule.get("pro_only", False) and not self.is_pro:
                continue
            
            try:
                # Find all matches for this pattern
                pattern = re.compile(rule["regex"])
                matches = pattern.finditer(text)
                
                for match in matches:
                    findings.append({
                        "type": rule["type"],
                        "match": match.group(0),
                        "rule": rule["name"],
                        "start": match.start(),
                        "end": match.end(),
                        "priority": rule.get("priority", 999)
                    })
                    
            except re.error as e:
                # Log regex compilation errors but continue processing
                print(f"Regex error in rule '{rule['name']}': {e}")
                continue
        
        # Sort findings by start position
        findings.sort(key=lambda x: x["start"])
        
        return findings
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about loaded rules.
        
        Returns:
            Dictionary containing:
                - total_rules: Total number of rules loaded
                - free_rules: Number of rules available in Free tier
                - pro_rules: Number of Pro-only rules
                - rule_types: Dictionary of rule counts by type
        """
        total = len(self.rules)
        pro_only = sum(1 for r in self.rules if r.get("pro_only", False))
        free = total - pro_only
        
        # Count by type
        types = {}
        for rule in self.rules:
            rule_type = rule.get("type", "unknown")
            types[rule_type] = types.get(rule_type, 0) + 1
        
        return {
            "total_rules": total,
            "free_rules": free,
            "pro_rules": pro_only,
            "rule_types": types
        }
    
    def get_available_rules(self) -> List[Dict[str, Any]]:
        """
        Get list of rules available to the current user.
        
        Returns:
            List of rules (excludes Pro-only rules if user is Free tier)
        """
        available = []
        
        for rule in self.rules:
            if rule.get("pro_only", False) and not self.is_pro:
                continue
            
            available.append({
                "name": rule["name"],
                "type": rule["type"],
                "description": rule.get("description", ""),
                "priority": rule.get("priority", 999),
                "pro_only": rule.get("pro_only", False)
            })
        
        return available
    
    def test_pattern(self, pattern: str, test_text: str) -> Optional[List[str]]:
        """
        Test a regex pattern against sample text.
        Useful for debugging and custom rule creation.
        
        Args:
            pattern: Regex pattern to test
            test_text: Text to test against
            
        Returns:
            List of matches, or None if pattern is invalid
        """
        try:
            compiled = re.compile(pattern)
            matches = compiled.findall(test_text)
            return matches
        except re.error:
            return None


# Module-level convenience function
def create_detector(is_pro: bool = False) -> DetectionEngine:
    """
    Create a detection engine with default rules path.
    
    Args:
        is_pro: Whether to enable Pro features
        
    Returns:
        Configured DetectionEngine instance
    """
    # Determine rules path relative to this file
    current_file = Path(__file__)
    rules_path = current_file.parent.parent / "resources" / "rules.json"
    
    return DetectionEngine(str(rules_path), is_pro=is_pro)


if __name__ == "__main__":
    # Simple test when run directly
    print("VaultMorph AI Shield - Detection Engine Test")
    print("=" * 50)
    
    # Create detector
    detector = create_detector(is_pro=False)
    
    # Show stats
    stats = detector.get_stats()
    print(f"\nLoaded {stats['total_rules']} rules:")
    print(f"  - Free tier: {stats['free_rules']} rules")
    print(f"  - Pro tier: {stats['pro_rules']} rules")
    print(f"\nRule types: {stats['rule_types']}")
    
    # Test detection
    test_text = """
    Here's my OpenAI key: sk-proj-abc123xyz456def789ghi012jkl345
    And my AWS key: AKIAIOSFODNN7EXAMPLE
    My email is user@example.com
    """
    
    print("\n" + "=" * 50)
    print("Testing detection on sample text...")
    print("=" * 50)
    
    findings = detector.detect(test_text)
    
    if findings:
        print(f"\nFound {len(findings)} sensitive items:")
        for i, finding in enumerate(findings, 1):
            print(f"\n{i}. {finding['rule']}")
            print(f"   Type: {finding['type']}")
            print(f"   Match: {finding['match']}")
            print(f"   Priority: {finding['priority']}")
    else:
        print("\nNo sensitive data detected.")
