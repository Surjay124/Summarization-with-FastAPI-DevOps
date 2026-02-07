import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add Code directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.models.sql_models import SummarizationLog

def check_db():
    print(f"Connecting to DB at: {settings.SQLALCHEMY_DATABASE_URI}")
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        count = session.query(SummarizationLog).count()
        print(f"Total Logs: {count}")
        
        logs = session.query(SummarizationLog).order_by(SummarizationLog.id.desc()).limit(5).all()
        for log in logs:
            print(f"[{log.id}] Model: {log.model_name} | Time: {log.response_time_seconds:.2f}s | Summary: {log.output_summary[:50]}...")
    except Exception as e:
        print(f"Error querying DB: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_db()
