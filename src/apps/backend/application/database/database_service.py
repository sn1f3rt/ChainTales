from typing import Optional

from datetime import datetime

from application.errors import (
    TipNotFoundError,
    PostNotFoundError,
    UserWithAddressNotFoundError,
    UserWithUsernameNotFoundError,
)
from application.database.models.database_models import Tip, Post, User
from application.database.internal.database_manager import DatabaseManager


class DatabaseService:
    database_manager: DatabaseManager = DatabaseManager()

    @staticmethod
    def setup_database() -> None:
        DatabaseService.database_manager.setup_database()

    @staticmethod
    def load_user(address: str) -> Optional[User]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(User).filter(User.address == address).first()

    @staticmethod
    def check_username(username: str) -> Optional[User]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_address(address: str) -> Optional[User]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(User).filter(User.address == address).first()

    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(User).filter(User.username == username).first()

    @staticmethod
    def get_unverified_users() -> list[User]:
        with DatabaseService.database_manager.acquire_session() as session:
            return (
                session.query(User)
                .filter(User.verified == False, User.id_number != None)
                .all()
            )

    @staticmethod
    def add_user(address: str, nonce: str) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = User(address=address, nonce=nonce)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def activate_user(address: str) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if user is None:
                raise UserWithAddressNotFoundError(address=address)
            user.active = True
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def update_username(address: str, username: str) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if user is None:
                raise UserWithAddressNotFoundError(address=address)

            posts = session.query(Post).filter(Post.author == user.username).all()
            for post in posts:
                post.author = username

            tips = session.query(Tip).filter(Tip.sender == user.username).all()
            for tip in tips:
                tip.sender = username

            tips = session.query(Tip).filter(Tip.recipient == user.username).all()
            for tip in tips:
                tip.recipient = username

            user.username = username
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def add_admin(username: str) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if user is None:
                raise UserWithUsernameNotFoundError(username=username)
            user.admin = True
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def remove_admin(username: str) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise UserWithUsernameNotFoundError(username=username)
            user.admin = False
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def get_post(username: str, post_id: str) -> Post:
        with DatabaseService.database_manager.acquire_session() as session:
            post = (
                session.query(Post)
                .filter(Post.author == username, Post.id == post_id)
                .first()
            )
        if post is None:
            raise PostNotFoundError(post_id=post_id)
        return post

    @staticmethod
    def get_user_posts(username: str) -> list[Post]:
        with DatabaseService.database_manager.acquire_session() as session:
            posts = (
                session.query(Post)
                .filter(Post.author == username)
                .order_by(Post.posted_at.desc())
                .all()
            )
        return posts

    @staticmethod
    def get_latest_posts() -> list[Post]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(Post).order_by(Post.posted_at.desc()).all()

    @staticmethod
    def new_post(username: str, post_id: str, title: str, content: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            post = Post(
                author=username,
                id=post_id,
                title=title,
                content=content,
                posted_at=datetime.now(),
            )
            session.add(post)
            session.commit()

    @staticmethod
    def update_post(username: str, post_id: str, title: str, content: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            post = (
                session.query(Post)
                .filter(Post.author == username, Post.id == post_id)
                .first()
            )
            if post is None:
                raise PostNotFoundError(post_id=post_id)
            post.title = title
            post.content = content
            session.commit()

    @staticmethod
    def delete_post(username: str, post_id: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            post = (
                session.query(Post)
                .filter(Post.author == username, Post.id == post_id)
                .first()
            )
            if not post:
                raise PostNotFoundError(post_id=post_id)
            session.delete(post)
            session.commit()

    @staticmethod
    def record_tip(
        sender: str, recipient: str, amount: str, post_id: str, tx_hash: str
    ) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            tip = Tip(
                sender=sender,
                recipient=recipient,
                amount=amount,
                post_id=post_id,
                tx_hash=tx_hash,
            )
            session.add(tip)
            session.commit()

    @staticmethod
    def get_pending_tips(username: str) -> list[Tip]:
        with DatabaseService.database_manager.acquire_session() as session:
            return (
                session.query(Tip)
                .filter(Tip.recipient == username, Tip.notified == False)
                .all()
            )

    @staticmethod
    def get_sent_tips(username: str) -> list[Tip]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(Tip).filter(Tip.sender == username).all()

    @staticmethod
    def get_received_tips(username: str) -> list[Tip]:
        with DatabaseService.database_manager.acquire_session() as session:
            return session.query(Tip).filter(Tip.recipient == username).all()

    @staticmethod
    def mark_notified(tip_id: int) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            tip = session.query(Tip).filter(Tip.id == tip_id).first()
            if not tip:
                raise TipNotFoundError(tip_id=tip_id)
            tip.notified = True
            session.commit()

    @staticmethod
    def update_kyc_info(
        address: str,
        name: str,
        age: str,
        location: str,
        id_number: str,
        id_front: Optional[bytes] = None,
        id_back: Optional[bytes] = None,
    ) -> User:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if not user:
                raise UserWithAddressNotFoundError(address=address)
            user.name = name
            user.age = int(age)
            user.location = location
            user.id_number = id_number
            user.id_front = id_front
            user.id_back = id_back
            session.commit()
            session.refresh(user)
        return user

    @staticmethod
    def approve_user(address: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if not user:
                raise UserWithAddressNotFoundError(address=address)
            user.verified = True
            user.verified_at = datetime.now()
            user.kyc_status = 1
            user.id_front = None
            user.id_back = None
            session.commit()
            session.refresh(user)

    @staticmethod
    def reject_user(address: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if not user:
                raise UserWithAddressNotFoundError(address=address)
            user.kyc_status = -1
            user.name = None
            user.age = None
            user.location = None
            user.id_number = None
            user.id_front = None
            user.id_back = None
            session.commit()

    @staticmethod
    def pending_notification(address: str) -> bool:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
        if not user:
            raise UserWithAddressNotFoundError(address=address)
        return user.kyc_status != 0

    @staticmethod
    def get_kyc_status(address: str) -> int:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
        if not user:
            raise UserWithAddressNotFoundError(address=address)
        return user.kyc_status

    @staticmethod
    def reset_kyc_status(address: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if not user:
                raise UserWithAddressNotFoundError(address=address)
            user.kyc_status = 0
            session.commit()
            session.refresh(user)

    @staticmethod
    def revoke_kyc(address: str) -> None:
        with DatabaseService.database_manager.acquire_session() as session:
            user = session.query(User).filter(User.address == address).first()
            if not user:
                raise UserWithAddressNotFoundError(address=address)
            user.verified = False
            user.verified_at = None
            user.name = None
            user.age = None
            user.location = None
            user.id_number = None
            user.id_front = None
            user.id_back = None
            session.commit()
            session.refresh(user)
