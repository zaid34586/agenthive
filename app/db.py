"""Database session helper for AgentHive."""
from sqlmodel import Session, create_engine
from .models import DB_PATH, engine  # reuse engine from models

# The get_session function is defined in models.py
# This file just re-exports for convenience if needed