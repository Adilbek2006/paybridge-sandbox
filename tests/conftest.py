import uuid

import pytest
from fastapi.testclient import TestClient

from paybridge.main import app

API_KEY = "pb_test_demo_key_123"


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth():
    return {"Authorization": f"Bearer {API_KEY}"}


def idem():
    return {"Idempotency-Key": str(uuid.uuid4())}


def payment_body(**overrides):
    body = {"amount": 150000, "currency": "KZT", "provider": "mock",
            "return_url": "https://shop.example/return", "metadata": {"order_id": "1042"}}
    body.update(overrides)
    return body
