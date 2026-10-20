"""Unified payment state machine (FR-11). Owner: Adilbek."""
from enum import Enum


class PaymentStatus(str, Enum):
    REQUIRES_ACTION = "requires_action"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    PARTIALLY_REFUNDED = "partially_refunded"
    REFUNDED = "refunded"


S = PaymentStatus
ALLOWED_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    S.REQUIRES_ACTION: {S.PROCESSING, S.FAILED, S.CANCELED},
    S.PROCESSING: {S.SUCCEEDED, S.FAILED},
    S.SUCCEEDED: {S.PARTIALLY_REFUNDED, S.REFUNDED},
    S.PARTIALLY_REFUNDED: {S.PARTIALLY_REFUNDED, S.REFUNDED},
    S.FAILED: set(),
    S.CANCELED: set(),
    S.REFUNDED: set(),
}


class InvalidTransition(Exception):
    def __init__(self, current: PaymentStatus, target: PaymentStatus):
        super().__init__(f"Cannot move payment from {current.value} to {target.value}")
        self.current, self.target = current, target


def ensure_transition(current: PaymentStatus, target: PaymentStatus) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidTransition(current, target)
