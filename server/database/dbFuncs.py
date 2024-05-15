from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session


def saveToDatabase(db: Session, object):
    try:
        db.add(object)
        db.commit()
        db.refresh(object)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


def deleteFromDatabase(db: Session, object):
    try:
        db.delete(object)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
