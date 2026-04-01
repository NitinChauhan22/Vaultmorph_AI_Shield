"""
VaultMorph AI Shield - Session Manager

This module manages session-based token mapping (NAT-style) for sanitizing
and restoring sensitive data. Each session maintains an isolated mapping
between original sensitive data and safe tokens.

Author: VaultMorph
Version: 1.0.0
"""

import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime


class SessionManager:
    """
    Manages multiple isolated sessions for sanitize/restore operations.
    
    Each session maintains its own token mapping, ensuring complete isolation
    between different conversations or contexts.
    
    Attributes:
        sessions (Dict): Dictionary of session_id -> session data
    """
    
    def __init__(self):
        """Initialize the session manager with empty sessions."""
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, name: Optional[str] = None) -> str:
        """
        Create a new session with unique ID.
        
        Args:
            name: Optional human-readable name for the session
            
        Returns:
            session_id: Unique identifier for the session
        """
        session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            "name": name or f"Session {len(self.sessions) + 1}",
            "created": datetime.now().isoformat(),
            "mapping": {},
            "original_text": "",
            "sanitized_text": "",
            "findings": []
        }
        
        return session_id
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session and all its data.
        
        Args:
            session_id: ID of the session to delete
            
        Returns:
            True if deleted, False if session doesn't exist
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get session data by ID.
        
        Args:
            session_id: ID of the session
            
        Returns:
            Session data dictionary or None if not found
        """
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[Dict[str, Any]]:
        """
        Get list of all sessions with basic info.
        
        Returns:
            List of session info dictionaries
        """
        session_list = []
        
        for session_id, data in self.sessions.items():
            session_list.append({
                "id": session_id,
                "name": data["name"],
                "created": data["created"],
                "has_data": bool(data["mapping"])
            })
        
        return session_list
    
    def sanitize(self, session_id: str, text: str, findings: List[Dict[str, Any]]) -> str:
        """
        Sanitize text by replacing sensitive data with tokens.
        
        This function processes findings in reverse order (by position) to ensure
        that earlier replacements don't affect the positions of later ones.
        
        Args:
            session_id: ID of the session
            text: Original text containing sensitive data
            findings: List of detected sensitive items from DetectionEngine
            
        Returns:
            Sanitized text with tokens replacing sensitive data
            
        Raises:
            ValueError: If session doesn't exist
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        session = self.sessions[session_id]

        # PREVENT RE-SANITIZING TOKENS
        if "__VMX_" in text:
            return text        

        # Store original text
        session["original_text"] = text
        session["findings"] = findings
        
        # If no findings, return text as-is
        if not findings:
            session["sanitized_text"] = text
            return text
        
        import re
        import uuid
        
        session["mapping"] = {}
        mapping = session["mapping"]
        
        # Build unique matches list (avoid duplicates breaking things)
        unique_matches = list(set([f["match"] for f in findings if f["match"]]))
        
        if not unique_matches:
            session["sanitized_text"] = text
            return text
        
        # Sort longest first (VERY IMPORTANT)
        unique_matches.sort(key=len, reverse=True)
        
        def replacer(match):
            original = match.group(0)
            token = f"__VMX_{uuid.uuid4().hex}__"
            mapping[token] = {
                "value": original,
                "type": "detected",
                "rule": "auto",
                "priority": 0
            }
            return token
        
        pattern = "|".join(re.escape(m) for m in unique_matches)
        
        sanitized = re.sub(pattern, replacer, text)
        
        session["sanitized_text"] = sanitized
        
        return sanitized
        
    
    def restore(self, session_id: str, text: str) -> str:
        """
        Restore original data from sanitized text using token mapping.
        
        Args:
            session_id: ID of the session
            text: Sanitized text containing tokens
            
        Returns:
            Text with tokens replaced by original sensitive data
            
        Raises:
            ValueError: If session doesn't exist
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} does not exist")
        
        session = self.sessions[session_id]
        mapping = session["mapping"]
        
        # If no mapping, return text as-is
        if not mapping:
            return text
        
        # Replace each token with original value
        restored = text
        
        # Replace longest tokens first (prevents partial replacement issues)
        for token in sorted(mapping.keys(), key=len, reverse=True):
            restored = restored.replace(token, mapping[token]["value"])
        
        return restored
    
    def get_mapping_info(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get information about the token mappings in a session.
        
        Args:
            session_id: ID of the session
            
        Returns:
            List of mapping information
        """
        if session_id not in self.sessions:
            return []
        
        session = self.sessions[session_id]
        mapping = session["mapping"]
        
        info = []
        for token, data in mapping.items():
            info.append({
                "token": token,
                "type": data["type"],
                "rule": data["rule"],
                "priority": data["priority"],
                "preview": data["value"][:20] + "..." if len(data["value"]) > 20 else data["value"]
            })
        
        return info
    
    def export_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Export session data for saving/sharing (Pro feature).
        
        Args:
            session_id: ID of the session to export
            
        Returns:
            Complete session data or None if session doesn't exist
        """
        return self.sessions.get(session_id)
    
    def import_session(self, session_data: Dict[str, Any], new_name: Optional[str] = None) -> str:
        """
        Import a session from exported data (Pro feature).
        
        Args:
            session_data: Previously exported session data
            new_name: Optional new name for the imported session
            
        Returns:
            New session_id for the imported session
        """
        new_id = str(uuid.uuid4())
        
        # Copy data but assign new ID
        imported = session_data.copy()
        if new_name:
            imported["name"] = new_name
        
        self.sessions[new_id] = imported
        
        return new_id
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear session data but keep the session.
        
        Args:
            session_id: ID of the session to clear
            
        Returns:
            True if cleared, False if session doesn't exist
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        session["mapping"] = {}
        session["original_text"] = ""
        session["sanitized_text"] = ""
        session["findings"] = []
        
        return True
    
    def get_session_count(self) -> int:
        """
        Get the total number of active sessions.
        
        Returns:
            Number of sessions
        """
        return len(self.sessions)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all sessions.
        
        Returns:
            Dictionary with session statistics
        """
        total = len(self.sessions)
        with_data = sum(1 for s in self.sessions.values() if s["mapping"])
        total_mappings = sum(len(s["mapping"]) for s in self.sessions.values())
        
        return {
            "total_sessions": total,
            "sessions_with_data": with_data,
            "total_token_mappings": total_mappings
        }


if __name__ == "__main__":
    # Simple test when run directly
    print("VaultMorph AI Shield - Session Manager Test")
    print("=" * 50)
    
    # Create manager
    manager = SessionManager()
    
    # Create a session
    session_id = manager.create_session("Test Session")
    print(f"\nCreated session: {session_id}")
    
    # Simulate some findings
    test_text = "My key is sk-abc123 and my email is user@example.com"
    
    findings = [
        {
            "type": "api_key",
            "match": "sk-abc123",
            "rule": "OpenAI API Key",
            "start": 10,
            "end": 19,
            "priority": 1
        },
        {
            "type": "pii",
            "match": "user@example.com",
            "rule": "Email Address",
            "start": 36,
            "end": 52,
            "priority": 3
        }
    ]
    
    # Sanitize
    print(f"\nOriginal: {test_text}")
    sanitized = manager.sanitize(session_id, test_text, findings)
    print(f"Sanitized: {sanitized}")
    
    # Show mapping info
    print("\nToken Mappings:")
    for info in manager.get_mapping_info(session_id):
        print(f"  {info['token']} -> {info['type']} ({info['rule']})")
    
    # Restore
    restored = manager.restore(session_id, sanitized)
    print(f"\nRestored: {restored}")
    
    # Verify
    print(f"\nMatch: {restored == test_text}")
    
    # Stats
    stats = manager.get_stats()
    print(f"\nStats: {stats}")
