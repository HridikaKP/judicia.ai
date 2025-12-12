# db.py
import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Required env vars
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")  # default for Docker
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DATABASE")

missing = [k for k, v in {
    "MYSQL_USER": MYSQL_USER,
    "MYSQL_PASSWORD": MYSQL_PASSWORD,
    "MYSQL_DATABASE": MYSQL_DB
}.items() if not v]

if missing:
    raise RuntimeError(f"Missing required DB env vars: {missing}. Check your .env. (see .env example)")

# Hostname resolution fallback
try:
    socket.gethostbyname(MYSQL_HOST)
except Exception:
    fallback_host = os.getenv("MYSQL_HOST_FALLBACK", "127.0.0.1")
    print(f"⚠️ MYSQL_HOST '{MYSQL_HOST}' not resolvable. Falling back to {fallback_host}.")
    MYSQL_HOST = fallback_host

DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

print(f"Using DATABASE_URL={DATABASE_URL}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
