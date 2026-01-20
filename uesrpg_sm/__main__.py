"""Allow running package with python -m uesrpg_sm."""
import sys
import os
from pathlib import Path

# Add parent directory to path so we can import app
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from app import main

if __name__ == '__main__':
    main()
