"""Payment service (FR-03…FR-07, FR-14). Owner: Adilbek."""
import secrets
import string
import threading

from ..domain.models import CreatePaymentRequest, Payment, StatusChange, utcnow
from ..domain.state_machine import PaymentStatus, ensure_transition
from ..providers.registry import get_provider

_ALPHABET = string.digits + string.ascii_uppercase


def new_id(prefix: str) -> str:
    return prefix + "_" + "".join(secrets.choice(_ALPHABET) for _ in range(26))


class PaymentNotFound(Exception):
    pass


class RefundTooLarge(Exception):
    pass


class PaymentService:
    def __init__(self) -> None:
        self._payments: dict[str, Payment] = {}
        self._lock = threading.Lock()

    def create(self, merchant_id: str, req: CreatePaymentRequest) -> Payment:
        provider = get_provider(req.provider)
        if provider is None:
            raise ValueError(f"Provider '{req.provider}' is not available in this build")
        payment_id = new_id("pay")
        result = provider.create_payment(payment_id, req)
        payment = Payment(
            id=payment_id, merchant_id=merchant_id, status=PaymentStatus.REQUIRES_ACTION,
            amount=req.amount, currency=req.currency, provider=req.provider,
            provider_payment_id=result.provider_payment_id, checkout_url=result.checkout_url,
            description=req.description, metadata=req.metadata,
        )
        payment.status_history.append(StatusChange(from_status=None, to_status=payment.status, source="api"))
        if result.status in (PaymentStatus.PROCESSING, PaymentStatus.SUCCEEDED):
            self._transition(payment, PaymentStatus.PROCESSING, source="provider")
        if result.status in (PaymentStatus.SUCCEEDED, PaymentStatus.FAILED):
            self._transition(payment, result.status, source="provider")
        with self._lock:
            self._payments[payment.id] = payment
        return payment

    def get(self, merchant_id: str, payment_id: str) -> Payment:
        payment = self._payments.get(payment_id)
        if payment is None or payment.merchant_id != merchant_id:  # BOLA protection (FR-02)
            raise PaymentNotFound(payment_id)
        return payment

    def list(self, merchant_id: str) -> list[Payment]:
        return sorted((p for p in self._payments.values() if p.merchant_id == merchant_id),
                      key=lambda p: p.created_at, reverse=True)

    def cancel(self, merchant_id: str, payment_id: str) -> Payment:
        payment = self.get(merchant_id, payment_id)
        self._transition(payment, PaymentStatus.CANCELED, source="api")
        return payment

    def refund(self, merchant_id: str, payment_id: str, amount: int | None) -> Payment:
        payment = self.get(merchant_id, payment_id)
        remaining = payment.amount - payment.amount_refunded
        amount = amount or remaining
        if amount > remaining:
            raise RefundTooLarge(f"Requested {amount}, refundable {remaining}")
        target = PaymentStatus.REFUNDED if amount == remaining else PaymentStatus.PARTIALLY_REFUNDED
        ensure_transition(payment.status, target)
        get_provider(payment.provider).refund(payment.provider_payment_id, amount)
        payment.amount_refunded += amount
        self._transition(payment, target, source="api")
        return payment

    @staticmethod
    def _transition(payment: Payment, target: PaymentStatus, source: str) -> None:
        ensure_transition(payment.status, target)
        payment.status_history.append(StatusChange(from_status=payment.status, to_status=target, source=source))
        payment.status = target
        payment.updated_at = utcnow()
