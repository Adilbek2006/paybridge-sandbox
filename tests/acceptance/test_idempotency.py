"""FR-08 / NFR-02: no duplicate payments under retries. Owner: Adilbek."""
from concurrent.futures import ThreadPoolExecutor

from tests.conftest import payment_body


def test_same_key_same_body_returns_same_payment(client, auth):
    h = auth | {"Idempotency-Key": "retry-key-0001"}
    a = client.post("/v1/payments", json=payment_body(), headers=h)
    b = client.post("/v1/payments", json=payment_body(), headers=h)
    assert a.status_code == b.status_code == 201
    assert a.json()["id"] == b.json()["id"]


def test_same_key_different_body_is_rejected(client, auth):
    h = auth | {"Idempotency-Key": "retry-key-0002"}
    client.post("/v1/payments", json=payment_body(), headers=h)
    r = client.post("/v1/payments", json=payment_body(amount=999), headers=h)
    assert r.status_code == 422


def test_missing_key_is_rejected(client, auth):
    assert client.post("/v1/payments", json=payment_body(), headers=auth).status_code == 422


def test_ten_parallel_requests_create_one_payment(client, auth):
    h = auth | {"Idempotency-Key": "parallel-key-0003"}
    before = len(client.get("/v1/payments", headers=auth).json()["data"])
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(lambda _: client.post("/v1/payments", json=payment_body(), headers=h), range(10)))
    assert {r.json()["id"] for r in results} == {results[0].json()["id"]}
    after = len(client.get("/v1/payments", headers=auth).json()["data"])
    assert after - before == 1
