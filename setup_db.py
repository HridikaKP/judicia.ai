#!/usr/bin/env python3
"""
Script to set up MySQL database and user for Judicia.ai
"""
import os
import sys
from pathlib import Path

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Try to connect as root and create the user/database
try:
    import pymysql
    
    root_password = os.getenv("MYSQL_ROOT_PASSWORD", "Root@123")
    db_host = os.getenv("MYSQL_HOST", "localhost")
    db_port = int(os.getenv("MYSQL_PORT", "3306"))
    db_name = os.getenv("MYSQL_DATABASE", "judiciadb")
    db_user = os.getenv("MYSQL_USER", "judicia")
    db_password = os.getenv("MYSQL_PASSWORD", "Judicia%402025")
    
    print(f"🔧 Setting up MySQL database...")
    print(f"  Host: {db_host}:{db_port}")
    print(f"  Database: {db_name}")
    print(f"  User: {db_user}")
    
    # Connect as root
    print("\n1️⃣ Connecting to MySQL as root...")
    conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user="root",
        password=root_password
    )
    cursor = conn.cursor()
    print("   ✅ Connected as root")
    
    # Create database if it doesn't exist
    print(f"\n2️⃣ Creating database '{db_name}' if not exists...")
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
    print(f"   ✅ Database ready")
    
    # Create user if it doesn't exist
    print(f"\n3️⃣ Creating user '{db_user}'@'%' if not exists...")
    cursor.execute(f"DROP USER IF EXISTS '{db_user}'@'%';")
    cursor.execute(f"CREATE USER '{db_user}'@'%' IDENTIFIED BY '{db_password}';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'%';")
    
    # Also create localhost version
    cursor.execute(f"DROP USER IF EXISTS '{db_user}'@'localhost';")
    cursor.execute(f"CREATE USER '{db_user}'@'localhost' IDENTIFIED BY '{db_password}';")
    cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{db_user}'@'localhost';")
    
    cursor.execute("FLUSH PRIVILEGES;")
    print(f"   ✅ User created with all privileges")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    # Now test connection as the new user
    print(f"\n4️⃣ Testing connection as '{db_user}'...")
    test_conn = pymysql.connect(
        host=db_host,
        port=db_port,
        user=db_user,
        password=db_password,
        database=db_name
    )
    test_cursor = test_conn.cursor()
    test_cursor.execute("SELECT 1;")
    test_cursor.fetchone()
    test_cursor.close()
    test_conn.close()
    print(f"   ✅ Connection successful!")
    
    print("\n✨ Database setup complete! You can now run the backend.")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"\nTroubleshooting:")
    print(f"  1. Make sure MySQL is running")
    print(f"  2. Check that MYSQL_ROOT_PASSWORD in .env is correct")
    print(f"  3. Verify MySQL is accessible at {os.getenv('MYSQL_HOST', 'localhost')}:{os.getenv('MYSQL_PORT', '3306')}")
    sys.exit(1)
