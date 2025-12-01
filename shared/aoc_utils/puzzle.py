"""
Puzzle input and content fetching for Advent of Code.

Provides functions to download and cache puzzle inputs and content
for specific days and years.
"""

import logging
from pathlib import Path

import requests
from .auth import get_session_token

# Set up logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_puzzle_input(year: int, day: int, overwrite: bool = False) -> Path:
    """Download puzzle input for a specific year and day.

    Downloads and caches the puzzle input locally. The input file never changes
    once created, so by default it won't be re-downloaded if it already exists.

    Args:
        year: AoC year (e.g., 2024, 2025)
        day: Day of the month (1-25)
        overwrite: If True, re-download even if file already exists

    Returns:
        Path to the input file

    Raises:
        ValueError: If year/day is invalid or input cannot be fetched
        requests.RequestException: If network request fails
    """
    # Validate inputs
    if not (2015 <= year <= 2030):
        raise ValueError(f"Invalid year: {year}. Must be between 2015 and 2030.")
    if not (1 <= day <= 25):
        raise ValueError(f"Invalid day: {day}. Must be between 1 and 25.")

    # Determine cache path
    cache_dir = Path.cwd() / str(year) / f"day{day:02d}"
    cache_file = cache_dir / "input.txt"

    # Check if file already exists
    if cache_file.exists() and not overwrite:
        logger.info(f"Input file already exists: {cache_file}")
        return cache_file

    # Fetch from AoC website
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    headers = {
        'User-Agent': 'aoc-utils/0.1.0 (https://github.com/mosqueteiro/AdventOfCode)',
        'Cookie': f"session={get_session_token()}"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # Create cache directory if it doesn't exist
        cache_dir.mkdir(parents=True, exist_ok=True)

        # Save to cache
        input_text = response.text.rstrip('\n')
        cache_file.write_text(input_text + '\n', encoding='utf-8')

        logger.info(f"Created input file: {cache_file}")
        return cache_file

    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Puzzle not found for {year} day {day}")
        elif e.response.status_code == 400:
            raise ValueError("Invalid session token or authentication failed")
        else:
            raise requests.RequestException(f"HTTP {e.response.status_code}: {e.response.reason}")
    except requests.Timeout:
        raise requests.RequestException("Request timed out")
    except requests.ConnectionError:
        raise requests.RequestException("Connection failed")
