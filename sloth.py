#!/usr/bin/env python3
"""
Sloth Digest — Root CLI Entry Point
Execute overnight batch jobs:
    python sloth.py run
    python sloth.py tidy
"""

from backend.sloth import main

if __name__ == "__main__":
    main()
