"""Allow running as python -m uesrpg_sm."""
import os
import sys

# Add the parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import main

if __name__ == '__main__':
    main()
