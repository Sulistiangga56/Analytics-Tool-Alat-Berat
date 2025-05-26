from sqlalchemy import create_engine
import os

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "intermilan12")
DB_NAME = os.getenv("DB_NAME", "analytics_db")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Local
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Supabase
DATABASE_URL = f"postgresql://postgres:intermilan12@db.trnvtnvfxrjzibactryb.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)