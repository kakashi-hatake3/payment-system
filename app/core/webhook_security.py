import hashlib
from decimal import Decimal
from app.config import settings


def generate_signature(transaction_id: str, user_id: int, account_id: int, amount: Decimal) -> str:
    # Создаем строку в алфавитном порядке ключей
    signature_string = f"{account_id}{amount}{transaction_id}{user_id}{settings.WEBHOOK_SECRET_KEY}"
    return hashlib.sha256(signature_string.encode()).hexdigest()


def verify_signature(transaction_id: str, user_id: int, account_id: int, amount: Decimal, signature: str) -> bool:
    expected_signature = generate_signature(transaction_id, user_id, account_id, amount)
    return expected_signature == signature
