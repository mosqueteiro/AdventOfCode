#!/usr/bin/env python3
"""
Setup CLI for aoc_utils authentication.
"""

import sys
from aoc_utils import get_session_token


def main():
    """Setup AoC session token."""
    try:
        token = get_session_token()
        print(f"✅ Authentication setup complete!")
        print(f"Session token configured successfully.")
    except ValueError as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    main()