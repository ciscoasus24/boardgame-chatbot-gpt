from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, crud
import engine as gpt_engine

# 테이블이 없으면 자동으로 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 각 요청에서 DB 세션을 생성/닫는 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET: 특정 게임의 전체 메시지 조회
@app.get("/chat/{game_name}")
def read_chat(game_name: str, db: Session = Depends(get_db)):
    messages = crud.get_messages_by_game(db, game_name)
    return [{"role": m.role, "content": m.content, "timestamp": m.timestamp} for m in messages]

# POST: 특정 게임에 메시지 추가
@app.post("/chat/{game_name}")
def create_message(game_name: str, role: str, content: str, db: Session = Depends(get_db)):
    if role not in ["user", "assistant"]:
        raise HTTPException(status_code=400, detail="role must be 'user' or 'assistant'")
    message = crud.add_message(db, game_name, role, content)
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "timestamp": message.timestamp
    }

@app.post("/chat/{game_name}/reply")
def ask_and_reply(game_name: str, question: str, db: Session = Depends(get_db)):
    # 1. 사용자 질문 저장
    crud.add_message(db, game_name, "user", question)

    # 2. GPT에게 응답 요청
    answer = gpt_engine.get_game_rule_detailed(game_name, question)

    # 3. GPT 응답 저장
    crud.add_message(db, game_name, "assistant", answer)

    # 4. 클라이언트에 응답 반환
    return {"question": question, "answer": answer}