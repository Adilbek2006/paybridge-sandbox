"""Provider registry. Stripe and PayPal adapters are added in DIP-27 / DIP-28."""
from .base import PaymentProvider
from .mock import MockProvider

_PROVIDERS: dict[str, PaymentProvider] = {"mock": MockProvider()}


def get_provider(name: str) -> PaymentProvider | None:
    return _PROVIDERS.get(name)
