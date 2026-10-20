"""Domain models. Owner: Adilbek."""
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, HttpUrl

from .state_machine import PaymentStatus

Provider = Literal["stripe", "paypal", "mock"]
MockScenario = Literal["success", "decline", "timeout", "delayed_success", "duplicate_webhook"]


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class CreatePaymentRequest(BaseModel):
    amount: int = Field(ge=1, le=100_000_000, description="Minor units")
    currency: Literal["KZT", "USD", "EUR"]
    provider: Provider = "mock"
    description: str | None = Field(default=None, max_length=200)
    return_url: HttpUrl
    metadata: dict[str, str] = Field(default_factory=dict, max_length=20)
    mock_scenario: MockScenario | None = None


class RefundRequest(BaseModel):
    amount: int | None = Field(default=None, ge=1)
    reason: str | None = Field(default=None, max_length=200)


class StatusChange(BaseModel):
    from_status: PaymentStatus | None
    to_status: PaymentStatus
    source: str
    at: datetime = Field(default_factory=utcnow)


class Payment(BaseModel):
    id: str
    object: Literal["payment"] = "payment"
    merchant_id: str
    status: PaymentStatus
    amount: int
    currency: str
    amount_refunded: int = 0
    provider: Provider
    provider_payment_id: str | None = None
    checkout_url: str | None = None
    description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    status_history: list[StatusChange] = Field(default_factory=list)
