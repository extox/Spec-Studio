from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.user import User
from app.models.login_history import LoginHistory
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token
from app.core.exceptions import ConflictError, UnauthorizedError


async def register_user(db: AsyncSession, email: str, password: str, display_name: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    if result.scalar_one_or_none():
        raise ConflictError("Email already registered")

    # Check if this is the first user → make admin
    count_result = await db.execute(select(func.count(User.id)))
    user_count = count_result.scalar() or 0
    is_first_user = user_count == 0

    user = User(
        email=email,
        hashed_password=hash_password(password),
        display_name=display_name,
        is_admin=is_first_user,
    )
    db.add(user)
    await db.flush()
    return user


async def login_user(db: AsyncSession, email: str, password: str, ip_address: str | None = None, user_agent: str | None = None) -> dict:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise UnauthorizedError("Invalid email or password")

    # Record login history
    history = LoginHistory(
        user_id=user.id,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    db.add(history)
    await db.flush()

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }
