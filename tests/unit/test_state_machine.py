"""FR-11: only allowed transitions. Owner: Adilbek."""
import pytest

from paybridge.domain.state_machine import InvalidTransition, PaymentStatus as S, ensure_transition


@pytest.mark.parametrize("src,dst", [
    (S.REQUIRES_ACTION, S.PROCESSING), (S.PROCESSING, S.SUCCEEDED),
    (S.SUCCEEDED, S.PARTIALLY_REFUNDED), (S.PARTIALLY_REFUNDED, S.REFUNDED),
    (S.REQUIRES_ACTION, S.CANCELED), (S.PROCESSING, S.FAILED),
])
def test_allowed(src, dst):
    ensure_transition(src, dst)


@pytest.mark.parametrize("src,dst", [
    (S.SUCCEEDED, S.CANCELED), (S.FAILED, S.SUCCEEDED), (S.REFUNDED, S.SUCCEEDED),
    (S.CANCELED, S.PROCESSING), (S.REQUIRES_ACTION, S.REFUNDED),
])
def test_illegal(src, dst):
    with pytest.raises(InvalidTransition):
        ensure_transition(src, dst)
