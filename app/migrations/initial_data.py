from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User, Admin, Account
from app.core.security import get_password_hash


async def create_initial_data(db: AsyncSession):
    # Создаем тестового пользователя
    test_user = User(
        email="user@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("userpassword123")
    )
    db.add(test_user)
    await db.flush()

    # Создаем счет для тестового пользователя
    test_account = Account(
        user_id=test_user.id,
        balance=0
    )
    db.add(test_account)

    # Создаем тестового администратора
    test_admin = Admin(
        email="admin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("adminpassword123")
    )
    db.add(test_admin)

    await db.commit()
