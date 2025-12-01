"""
Advent of Code authentication handling.

Manages session tokens for accessing AoC website and puzzle inputs.
"""

import os
import re
from pathlib import Path
from typing import Optional

import requests
from dotenv import load_dotenv, set_key


class AoCSession:
    """Manages Advent of Code session authentication."""
    
    def __init__(self, env_file: Optional[Path] = None):
        """Initialize session manager.
        
        Args:
            env_file: Path to .env file. Defaults to ~/.config/aoc_utils/.env
        """
        if env_file is None:
            config_dir = self._get_config_dir()
            env_file = config_dir / ".env"
        
        self.env_file = env_file
        self._session_token = None
    
    def _get_config_dir(self) -> Path:
        """Get aoc_utils configuration directory."""
        config_dir = Path.home() / ".config" / "aoc_utils"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def get_session_token(self) -> str:
        """Get valid AoC session token.
        
        Returns:
            Valid session token for AoC API requests
            
        Raises:
            ValueError: If no valid token is available
        """
        if self._session_token is None:
            token = self._load_token_from_env()
            if token is None or not self._validate_token(token):
                token = self._prompt_for_token()
                if token and self._validate_token(token):
                    self._save_token(token)
                else:
                    raise ValueError("Invalid session token provided")
            self._session_token = token
        
        return self._session_token
    
    def _load_token_from_env(self) -> Optional[str]:
        """Load token from environment variables or .env file."""
        # Load .env file into environment if it exists
        if self.env_file.exists():
            load_dotenv(self.env_file)
        
        # Now just check environment (works for both sources)
        return os.getenv("AOC_SESSION_TOKEN")
    
    def _validate_token(self, token: str) -> bool:
        """Validate if token is a valid AoC session token.
        
        Args:
            token: Session token to validate
            
        Returns:
            True if token is valid, False otherwise
        """
        if not token or not re.match(r'^[a-f0-9]+$', token):
            return False
        
        try:
            response = requests.get(
                "https://adventofcode.com/2024/day/1/input",
                cookies={"session": token},
                timeout=10
            )
            return response.status_code == 200
        except requests.RequestException:
            return False
    
    def _prompt_for_token(self) -> Optional[str]:
        """Prompt user to enter their session token.
        
        Returns:
            Session token from user input, or None if cancelled
        """
        from getpass import getpass
        
        print("\n" + "="*60)
        print("Advent of Code Session Token Setup")
        print("="*60)
        print("\nTo access puzzle inputs, you need your session token.")
        print("\nHow to get your session token:")
        print("1. Log in to https://adventofcode.com")
        print("2. Open browser developer tools (F12)")
        print("3. Go to Application/Storage → Cookies → adventofcode.com")
        print("4. Copy the value of the 'session' cookie")
        print("\nNote: This token is sensitive and should be kept private!")
        print("="*60 + "\n")
        
        try:
            token = getpass("Enter your session token (or press Enter to cancel): ")
            return token.strip() if token else None
        except (KeyboardInterrupt, EOFError):
            return None
    
    def _save_token(self, token: str) -> None:
        """Save token to .env file.
        
        Args:
            token: Valid session token to save
        """
        # Ensure .env file exists with proper permissions
        if not self.env_file.exists():
            self.env_file.touch(mode=0o600)
        
        # Set restrictive permissions
        self.env_file.chmod(0o600)
        
        # Save token
        set_key(str(self.env_file), "AOC_SESSION_TOKEN", token)
        print(f"Session token saved to {self.env_file}")


# Global session instance
_session_manager = None


def get_session_token() -> str:
    """Get valid AoC session token using global session manager.
    
    Returns:
        Valid session token for AoC API requests
        
    Raises:
        ValueError: If no valid token is available
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = AoCSession()
    return _session_manager.get_session_token()
