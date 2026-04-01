"""
VaultMorph AI Shield - Storage Manager

This module handles encrypted local storage for session data, settings, and
other persistent information. Uses Fernet symmetric encryption for data protection.

Author: VaultMorph
Version: 1.0.0
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet, InvalidToken


class StorageManager:
    """
    Manages encrypted local storage for application data.
    
    Features:
    - Fernet symmetric encryption (AES-128)
    - Automatic key generation and management
    - JSON-based data structure
    - Isolated storage in user home directory
    - Error handling for corrupted data
    
    Attributes:
        base_path (Path): Base directory for VaultMorph data
        key_file (Path): Path to encryption key file
        data_file (Path): Path to encrypted data file
        key (bytes): Fernet encryption key
        cipher (Fernet): Fernet cipher instance
    """
    
    def __init__(self, app_name: str = "vaultmorph"):
        """
        Initialize storage manager.
        
        Args:
            app_name: Name of application directory (default: "vaultmorph")
        """
        # Create base directory in user home
        self.base_path = Path.home() / f".{app_name}"
        self.base_path.mkdir(exist_ok=True, parents=True)
        
        # File paths
        self.key_file = self.base_path / "key.key"
        self.data_file = self.base_path / "data.enc"
        
        # Initialize encryption
        self.key = self._load_or_create_key()
        self.cipher = Fernet(self.key)
    
    def _load_or_create_key(self) -> bytes:
        """
        Load existing encryption key or create new one.
        
        Returns:
            Encryption key as bytes
        """
        if self.key_file.exists():
            # Load existing key
            return self.key_file.read_bytes()
        else:
            # Generate new key
            key = Fernet.generate_key()
            self.key_file.write_bytes(key)
            
            # Set restrictive permissions on key file (Unix-like systems)
            try:
                self.key_file.chmod(0o600)  # Read/write for owner only
            except Exception:
                # Windows doesn't support chmod in the same way
                pass
            
            return key
    
    def save(self, data: Dict[str, Any]) -> bool:
        """
        Encrypt and save data to disk.
        
        Args:
            data: Dictionary to save (must be JSON-serializable)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Convert to JSON
            json_data = json.dumps(data, indent=2)
            
            # Encrypt
            encrypted = self.cipher.encrypt(json_data.encode('utf-8'))
            
            # Write to file
            self.data_file.write_bytes(encrypted)
            
            return True
            
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load(self) -> Dict[str, Any]:
        """
        Load and decrypt data from disk.
        
        Returns:
            Dictionary containing saved data, or empty dict if no data/error
        """
        if not self.data_file.exists():
            return {}
        
        try:
            # Read encrypted data
            encrypted = self.data_file.read_bytes()
            
            # Decrypt
            decrypted = self.cipher.decrypt(encrypted)
            
            # Parse JSON
            data = json.loads(decrypted.decode('utf-8'))
            
            return data
            
        except InvalidToken:
            print("Error: Invalid encryption key or corrupted data")
            return {}
        except json.JSONDecodeError:
            print("Error: Corrupted data structure")
            return {}
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a specific value from storage.
        
        Args:
            key: Key to retrieve
            default: Default value if key doesn't exist
            
        Returns:
            Value associated with key, or default
        """
        data = self.load()
        return data.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a specific value in storage.
        
        Args:
            key: Key to set
            value: Value to store (must be JSON-serializable)
            
        Returns:
            True if successful, False otherwise
        """
        data = self.load()
        data[key] = value
        return self.save(data)
    
    def delete(self, key: str) -> bool:
        """
        Delete a specific key from storage.
        
        Args:
            key: Key to delete
            
        Returns:
            True if successful (even if key didn't exist), False on error
        """
        data = self.load()
        if key in data:
            del data[key]
        return self.save(data)
    
    def clear(self) -> bool:
        """
        Clear all data from storage.
        
        Returns:
            True if successful, False otherwise
        """
        return self.save({})
    
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in storage.
        
        Args:
            key: Key to check
            
        Returns:
            True if key exists, False otherwise
        """
        data = self.load()
        return key in data
    
    def get_storage_path(self) -> str:
        """
        Get the path to the storage directory.
        
        Returns:
            Absolute path to storage directory
        """
        return str(self.base_path.absolute())
    
    def get_storage_size(self) -> int:
        """
        Get the size of stored data in bytes.
        
        Returns:
            Size in bytes, or 0 if file doesn't exist
        """
        if self.data_file.exists():
            return self.data_file.stat().st_size
        return 0
    
    def backup(self, backup_path: str) -> bool:
        """
        Create a backup of encrypted data.
        
        Args:
            backup_path: Path where backup should be saved
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if self.data_file.exists():
                import shutil
                shutil.copy2(self.data_file, backup_path)
                return True
            return False
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def restore(self, backup_path: str) -> bool:
        """
        Restore data from a backup.
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import shutil
            shutil.copy2(backup_path, self.data_file)
            
            # Verify the restore by attempting to load
            data = self.load()
            return data is not None
            
        except Exception as e:
            print(f"Error restoring backup: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get storage statistics.
        
        Returns:
            Dictionary with storage statistics
        """
        data = self.load()
        
        return {
            "storage_path": self.get_storage_path(),
            "data_size_bytes": self.get_storage_size(),
            "key_exists": self.key_file.exists(),
            "data_exists": self.data_file.exists(),
            "num_keys": len(data),
            "keys": list(data.keys())
        }


if __name__ == "__main__":
    # Test storage manager
    print("VaultMorph AI Shield - Storage Manager Test")
    print("=" * 60)
    
    # Create storage manager
    storage = StorageManager(app_name="vaultmorph_test")
    
    print("\n[1] Storage initialization:")
    print(f"  Storage path: {storage.get_storage_path()}")
    print(f"  Key file exists: {storage.key_file.exists()}")
    
    # Save some test data
    print("\n[2] Saving test data...")
    test_data = {
        "app_version": "1.0.0",
        "settings": {
            "theme": "dark",
            "language": "en"
        },
        "sessions": [
            {"id": "123", "name": "Test Session"}
        ]
    }
    
    success = storage.save(test_data)
    print(f"  Save successful: {success}")
    
    # Load data back
    print("\n[3] Loading data...")
    loaded = storage.load()
    print(f"  Data loaded: {len(loaded)} top-level keys")
    print(f"  Match original: {loaded == test_data}")
    
    # Test get/set
    print("\n[4] Testing get/set operations...")
    version = storage.get("app_version")
    print(f"  Retrieved version: {version}")
    
    storage.set("last_run", "2026-04-01")
    last_run = storage.get("last_run")
    print(f"  Set and retrieved last_run: {last_run}")
    
    # Test key operations
    print("\n[5] Testing key operations...")
    print(f"  'app_version' exists: {storage.exists('app_version')}")
    print(f"  'nonexistent' exists: {storage.exists('nonexistent')}")
    
    # Stats
    print("\n[6] Storage statistics:")
    stats = storage.get_stats()
    for key, value in stats.items():
        if key != "keys":
            print(f"  {key}: {value}")
    print(f"  Stored keys: {', '.join(stats['keys'])}")
    
    # Test encryption (data should be unreadable)
    print("\n[7] Encryption verification:")
    raw_content = storage.data_file.read_bytes()
    print(f"  Encrypted data (first 50 bytes): {raw_content[:50]}")
    print(f"  Data is encrypted: {b'app_version' not in raw_content}")
    
    # Cleanup
    print("\n[8] Cleanup...")
    storage.clear()
    print(f"  Storage cleared: {len(storage.load()) == 0}")
    
    print("\n" + "=" * 60)
    print("Storage Manager Test: ✓ COMPLETE")
