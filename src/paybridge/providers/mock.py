"""Deterministic mock provider (FR-09). Owner: Nurbol.

Prototype: scenarios resolve synchronously. In the next stage the provider will emit
simulated webhooks to /webhooks/mock so the full asynchronous path is exercised.
"""
from ..domain.models import CreatePaymentRequest
from ..domain.state_machine import PaymentStatus
from .base import ProviderError, ProviderPaymentResult

SCENARIO_RESULT = {
    "success": PaymentStatus.SUCCEEDED,
    "decline": PaymentStatus.FAILED,
    "delayed_success": PaymentStatus.PROCESSING,
    "duplicate_webhook": PaymentStatus.SUCCEEDED,
}


class MockProvider:
    name = "mock"

    def create_payment(self, payment_id: str, request: CreatePaymentRequest) -> ProviderPaymentResult:
        scenario = request.mock_scenario or "success"
        if scenario == "timeout":
            raise ProviderError("Mock provider timeout (scenario=timeout)")
        return ProviderPaymentResult(
            provider_payment_id=f"mock_{payment_id}",
            status=SCENARIO_RESULT[scenario],
            checkout_url=None,
        )

    def refund(self, provider_payment_id: str, amount: int) -> None:
        return None
