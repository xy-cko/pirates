import mysql.connector
import os
import logging
from sqlalchemy.orm import Session 
from db.schema import engine, RequestsLog

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def log_request_to_db(sentence, magic_number=None, eng_out=None, jap_out=None, mon_out=None, error=None):
    try:
        with Session(engine) as session:
            # Instantiate your SQLAlchemy model
            new_log = RequestsLog(
                sentence=sentence,
                magic_number=magic_number,
                english_output=eng_out,
                japanese_output=jap_out,
                mongolian_output=mon_out,
                error=error
            )
            
            # Add and commit the transaction
            session.add(new_log)
            session.commit()
            
            logger.info("Successfully logged to the db")
        
    except Exception as e:
        logger.error(f"Failed to log to database: {e}")
        
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()