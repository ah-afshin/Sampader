import uuid
from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .associations import likes_table



class Post(Base):
    __tablename__ = "posts"

    postID: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    date: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
    )
    text: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )
    
    category: Mapped[str] = mapped_column(String, nullable=True)
    contents: Mapped[str] = mapped_column(String(40), nullable=True)
    authorID: Mapped[str] = mapped_column(
        ForeignKey("users.userID"),
        nullable=False
    )
    parentID: Mapped[str] = mapped_column(
        ForeignKey("posts.postID"),
        nullable=True
    )

    author: Mapped["User"] = relationship(
        back_populates="posts"
    )
    parent: Mapped["Post"] = relationship(
        remote_side=[postID]
    )
    likes: Mapped[list["User"]] = relationship(
        secondary=likes_table,
        back_populates="likes"
    )

    def __repr__(self):
        return f"<Post '{self.text[:6]}...' by {self.author.username}>"
