from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:Adetoks%401971@localhost/knowireland_ai"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("✅ Database connection successful!")
    connection.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)