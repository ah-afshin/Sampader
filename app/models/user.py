import uuid
from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum as DBEnum
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .constants import VerifiedStatus
from .associations import followers_table
from .associations import blocks_table
from .associations import likes_table



class User(Base):
    __tablename__ = "users"

    userID: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(
        String(40),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(String(80))
    bio: Mapped[str] = mapped_column(String(200))
    profile: Mapped[str] = mapped_column(String(40))
    banner: Mapped[str] = mapped_column(String(40))

    joined_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )
    verified: Mapped[VerifiedStatus] = mapped_column(
        DBEnum(VerifiedStatus),
        default=VerifiedStatus.NOT_VERIFIED
    )
    lastseen: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC)
    )

    password: Mapped[str] = mapped_column(String(80), nullable=False)
    password_salt: Mapped[str] = mapped_column(String(32), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="author"
    )
    likes: Mapped[list["Post"]] = relationship(
        secondary=likes_table,
        back_populates="likes"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    followers: Mapped[list["User"]] = relationship(
        secondary=followers_table,
        primaryjoin=(userID == followers_table.c.followed_id),
        secondaryjoin=(userID == followers_table.c.follower_id),
        backref="followings"
    )
    blockers: Mapped[list["User"]] = relationship(
        secondary=blocks_table,
        primaryjoin=(userID == blocks_table.c.blocked_id),
        secondaryjoin=(userID == blocks_table.c.blocker_id),
        backref="blockings"
    )

    def __repr__(self):
        return f"<User {self.username} (ID: {self.userID})>"
