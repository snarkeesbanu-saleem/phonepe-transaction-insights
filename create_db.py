# create_db.py - Create the phonepe_pulse database

import sqlalchemy as sa
from sqlalchemy import create_engine, text

print('Creating database phonepe_pulse...')

# Connect to default 'postgres' database first
engine = create_engine(
    'postgresql+psycopg2://postgres:NewPassword123!@localhost:5432/postgres',
    echo=False
)

try:
    with engine.connect() as conn:
        conn.execute(text('COMMIT'))                    # Important for PostgreSQL
        conn.execute(text('CREATE DATABASE phonepe_pulse'))
        print('✅ Database "phonepe_pulse" created successfully!')
except Exception as e:
    error_str = str(e).lower()
    if 'already exists' in error_str:
        print('✅ Database "phonepe_pulse" already exists!')
    else:
        print('❌ Error creating database:')
        print(e)

print('\nNow testing connection to phonepe_pulse...')
