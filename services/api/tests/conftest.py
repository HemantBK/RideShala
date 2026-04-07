"""Pytest configuration — ensures 'app' module is importable."""

import sys
from pathlib import Path

# Add services/api to sys.path so 'from app.main import app' works
# regardless of where pytest is invoked from
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
