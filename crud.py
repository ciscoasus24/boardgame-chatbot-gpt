from sqlalchemy.orm import Session
from models import Message

def get_messages_by_game(db: Session, game_name: str):
    return db.query(Message).filter(Message.game_name == game_name).order_by(Message.timestamp).all()

def add_message(db: Session, game_name: str, role: str, content: str):
    message = Message(game_name=game_name, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def delete_all_messages(db: Session, game_name:str):
    db.query(Message).filter(Message.game_name == game_name).delete()
    db.commit()

def delete_oldest_message(db: Session, game_name: str):
    oldest_message = db.query(Message).filter(Message.game_name == game_name).order_by(Message.timestamp).first()
    if oldest_message:
        db.delete(oldest_message)
        db.commit()
        return oldest_message
    else:
        return None