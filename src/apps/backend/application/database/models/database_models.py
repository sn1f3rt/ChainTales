from typing import Optional

from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mysql import LONGBLOB

from application.database.internal.database_manager import DatabaseManager


class User(DatabaseManager.Base):
    __tablename__ = "users"

    address: Mapped[str] = mapped_column(
        String(42), primary_key=True, nullable=False
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(10), unique=True, nullable=True
    )
    nonce: Mapped[str] = mapped_column(String(11), nullable=False)
    active: Mapped[bool] = mapped_column(default=False, nullable=False)
    admin: Mapped[bool] = mapped_column(default=False, nullable=False)
    verified: Mapped[bool] = mapped_column(default=False, nullable=False)
    verified_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    kyc_status: Mapped[int] = mapped_column(default=0, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    id_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    id_front: Mapped[Optional[bytes]] = mapped_column(LONGBLOB, nullable=True)
    id_back: Mapped[Optional[bytes]] = mapped_column(LONGBLOB, nullable=True)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return self.active

    @property
    def is_verified(self) -> bool:
        return self.verified

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.address

    def __repr__(self) -> str:
        return f"<User {self.address}>"


class Post(DatabaseManager.Base):
    __tablename__ = "posts"

    author: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    id: Mapped[str] = mapped_column(String(8), primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=False)
    posted_at: Mapped[datetime] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return f"<Post {self.author} {self.id}>"


class Tip(DatabaseManager.Base):
    __tablename__ = "tips"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    sender: Mapped[str] = mapped_column(String(10), nullable=False)
    recipient: Mapped[str] = mapped_column(String(10), nullable=False)
    amount: Mapped[str] = mapped_column(String(10), nullable=False)
    post_id: Mapped[str] = mapped_column(String(8), nullable=False)
    tx_hash: Mapped[Optional[str]] = mapped_column(String(66), nullable=True)
    notified: Mapped[bool] = mapped_column(default=False, nullable=False)

    def __repr__(self) -> str:
        return f"<Tip {self.sender} {self.recipient}>"
