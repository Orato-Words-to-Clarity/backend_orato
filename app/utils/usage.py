
from datetime import date
from sqlalchemy.orm import Session
from app.db.models.usage import UsageLimit  # Import your ORM model

DAILY_LIMITS = {
    "llama": 500000,
    "whisper": 200000
}



def estimate_tokens(text: str) -> int:
    return int(len(text) / 4)  # 1 token ≈ 4 characters

def update_usage(user_id: str, model: str, tokens_used: int, db: Session):
    today = date.today()
    
    usage = db.query(UsageLimit).filter_by(user_id=user_id, date=today).first()

    if not usage:
        # Create new entry for today
        usage = UsageLimit(user_id=user_id, date=today)
        db.add(usage)

    # Update the correct model's token count
    if model == "llama":
        if usage.total_llama_tokens is None:
            usage.total_llama_tokens = 0
        usage.total_llama_tokens += tokens_used
    elif model == "whisper":
        if usage.total_whisper_tokens is None:
            usage.total_whisper_tokens = 0
        usage.total_whisper_tokens += tokens_used

    db.commit()


def check_usage_limit(user_id: str, model: str, db: Session) -> bool:
    today = date.today()
    usage = db.query(UsageLimit).filter_by(user_id=user_id, date=today).first()

    if not usage:
        return False  # No usage yet, so under limit

    total_tokens = usage.total_llama_tokens if model == "llama" else usage.total_whisper_tokens
    return total_tokens >= DAILY_LIMITS[model]
