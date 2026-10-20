"""FR-09: deterministic mock scenarios. Owner: Nurbol."""
import pytest

from tests.conftest import idem, payment_body


@pytest.mark.parametrize("scenario,status_code,final", [
    ("success", 201, "succeeded"),
    ("decline", 201, "failed"),
    ("delayed_success", 201, "processing"),
    ("timeout", 502, None),
])
def test_scenarios(client, auth, scenario, status_code, final):
    r = client.post("/v1/payments", json=payment_body(mock_scenario=scenario), headers=auth | idem())
    assert r.status_code == status_code
    if final:
        assert r.json()["status"] == final
