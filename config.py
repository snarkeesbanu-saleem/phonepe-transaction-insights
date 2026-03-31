# config.py - PostgreSQL Connection for PhonePe Project
# Password: NewPassword123!

import sqlalchemy as sa
from sqlalchemy import create_engine

DB_CONFIG = {
    'user': 'postgres',
    'password': 'NewPassword123!',     # Trying this password
    'host': 'localhost',
    'port': 5432,
    'database': 'phonepe_pulse'
}

DATABASE_URL = f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

def test_connection():
    try:
        with engine.connect() as conn:
            result = conn.execute(sa.text('SELECT version()'))
            version = result.scalar()
            print('✅ PostgreSQL Connection Successful!')
            print(f'PostgreSQL Version: {version}')
            print(f'Database: {DB_CONFIG["database"]}')
            return True
    except Exception as e:
        print('❌ Connection Failed!')
        print(f'Error: {e}')
        print('\nTips:')
        print('1. Make sure PostgreSQL server is running in pgAdmin')
        print('2. Confirm you have created the database "phonepe_pulse" in pgAdmin')
        return False

if __name__ == '__main__':
    test_connection()
