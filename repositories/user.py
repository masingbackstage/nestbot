from sqlalchemy import select
from sqlalchemy.orm import Session

from models import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_external_ref(self, external_ref: str) -> User | None:
        stmt = select(User).where(User.external_ref == external_ref)
        return self.db.execute(stmt).scalar_one_or_none()

    def create(self, external_ref: str, display_name: str | None = None) -> User:
        user = User(external_ref=external_ref, display_name=display_name)
        self.db.add(user)
        self.db.flush()
        return user

    def get_or_create_by_external_ref(
        self, external_ref: str, display_name: str | None
    ) -> tuple[User, bool]:
        user = self.get_by_external_ref(external_ref)
        if user is not None:
            return user, False
        return self.create(external_ref, display_name), True
