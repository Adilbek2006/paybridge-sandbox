"""Port for payment providers (NFR-05). Owner: Adilbek (interface)."""
from dataclasses import dataclass
from typing import Protocol

from ..domain.models import CreatePaymentRequest
from ..domain.state_machine import PaymentStatus


@dataclass
class ProviderPaymentResult:
    provider_payment_id: str
    status: PaymentStatus
    checkout_url: str | None = None


class ProviderError(Exception):
    """Provider returned an error or timed out (mapped to HTTP 502)."""


class PaymentProvider(Protocol):
    name: str

    def create_payment(self, payment_id: str, request: CreatePaymentRequest) -> ProviderPaymentResult: ...

    def refund(self, provider_payment_id: str, amount: int) -> None: ...
