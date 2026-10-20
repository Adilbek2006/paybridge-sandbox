"""FR-02, FR-03, FR-04, FR-06, FR-14 acceptance tests. Owner: Adilbek."""
from tests.conftest import idem, payment_body


def test_requires_api_key(client):
    assert client.post("/v1/payments", json=payment_body(), headers=idem()).status_code == 401


def test_create_and_get(client, auth):
    r = client.post("/v1/payments", json=payment_body(), headers=auth | idem())
    assert r.status_code == 201
    pay = r.json()
    assert pay["status"] == "succeeded" and pay["amount"] == 150000
    got = client.get(f"/v1/payments/{pay['id']}", headers=auth).json()
    assert [h["to_status"] for h in got["status_history"]] == ["requires_action", "processing", "succeeded"]


def test_invalid_amount_is_rfc9457(client, auth):
    r = client.post("/v1/payments", json=payment_body(amount=0), headers=auth | idem())
    assert r.status_code == 422
    assert r.headers["content-type"].startswith("application/problem+json")


def test_cannot_cancel_succeeded(client, auth):
    pay = client.post("/v1/payments", json=payment_body(), headers=auth | idem()).json()
    assert client.post(f"/v1/payments/{pay['id']}/cancel", headers=auth | idem()).status_code == 409


def test_partial_then_full_refund_and_over_refund(client, auth):
    pay = client.post("/v1/payments", json=payment_body(amount=10000), headers=auth | idem()).json()
    r1 = client.post(f"/v1/payments/{pay['id']}/refunds", json={"amount": 4000}, headers=auth | idem())
    assert r1.json()["status"] == "partially_refunded"
    over = client.post(f"/v1/payments/{pay['id']}/refunds", json={"amount": 7000}, headers=auth | idem())
    assert over.status_code == 422
    r2 = client.post(f"/v1/payments/{pay['id']}/refunds", json={}, headers=auth | idem())
    assert r2.json() == {"payment_id": pay["id"], "status": "refunded", "amount_refunded": 10000}
