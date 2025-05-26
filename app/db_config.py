from sqlalchemy import create_engine
import os

DB_USER = os.getenv("DB_USER", "postgres.trnvtnvfxrjzibactryb")
DB_PASS = os.getenv("DB_PASS", "intermilan12")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_HOST = os.getenv("DB_HOST", "aws-0-ap-southeast-1.pooler.supabase.com")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_POOL_MODE = os.getenv("DB_POOL_MODE", "session")

# Local
# DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Supabase
DATABASE_URL = f"postgresql://postgres.trnvtnvfxrjzibactryb:intermilan12@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres"

engine = create_engine(DATABASE_URL)