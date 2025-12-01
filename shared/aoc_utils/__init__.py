"""
Advent of Code utilities package.

Provides common functionality for AoC challenges including
authentication and input fetching.
"""

from .auth import AoCSession, get_session_token
from .puzzle import get_puzzle_input

__all__ = ["AoCSession", "get_session_token", "get_puzzle_input"]