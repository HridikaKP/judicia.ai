"""
Judicia.ai Backend Package
--------------------------
This file initializes the backend package by:
- Loading environment variables
- Setting up application-wide logging
- Initializing FastAPI app import
- Ensuring DB metadata is created once
"""

import os
import logging
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# -------------------------------------------------------------------------
# Logger Setup
# -------------------------------------------------------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("judicia-backend")
logger.info("Initializing Judicia.ai backend package...")

# -------------------------------------------------------------------------
# Import FastAPI app
# -------------------------------------------------------------------------
try:
    from .main import app
    logger.info("FastAPI app loaded successfully.")
except Exception as e:
    logger.error(f"Error loading FastAPI application: {e}")
    raise

# -------------------------------------------------------------------------
# Initialize DB schema
# -------------------------------------------------------------------------
try:
    from .db import engine
    from .crud import init_db
    init_db(engine)
    logger.info("Database initialized successfully.")
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
