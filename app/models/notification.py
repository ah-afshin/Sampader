import uuid
from datetime import datetime
from datetime import UTC

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Enum as DBEnum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import Base
from .constants import NotificationType



class Notification(Base):
    __tablename__ = 'notifications'

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.userID'),
        nullable=False
    )
    content: Mapped[str] = mapped_column(
        String,
        nullable=False
    )
    notification_type: Mapped[NotificationType] = mapped_column(
        DBEnum(NotificationType)
    )

    is_read: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC)
        )

    user: Mapped["User"] = relationship(
        back_populates="notifications"
    )

    def __repr__(self):
        return f'<{self.notification_type} for "{self.user_id}">'
