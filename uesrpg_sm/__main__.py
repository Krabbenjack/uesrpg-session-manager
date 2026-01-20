"""Allow running package with python -m uesrpg_sm."""
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import main

if __name__ == '__main__':
    main()
