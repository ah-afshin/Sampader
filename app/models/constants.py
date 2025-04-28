from enum import Enum


class VerifiedStatus(str, Enum):
    NOT_VERIFIED = "not verified"
    OFFICIAL = "official"
    ADMIN = "admin"
    COUNCIL = "school council"
    CELEBRITY = "celebrity"


class NotificationType(str, Enum):
    LIKE = "like"
    COMMENT = "comment"
    FOLLOW = "follow"
