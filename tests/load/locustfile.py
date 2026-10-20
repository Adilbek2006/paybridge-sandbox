"""NFR-01 load test (Locust). Owner: Nurbol.
Run: locust -f tests/load/locustfile.py --host http://localhost:8000 -u 50 -r 10 -t 5m --headless
"""
import uuid

from locust import HttpUser, constant_throughput, task


class Merchant(HttpUser):
    wait_time = constant_throughput(1)

    @task
    def create_payment(self):
        self.client.post("/v1/payments",
                         json={"amount": 1000, "currency": "KZT", "provider": "mock",
                               "return_url": "https://shop.example/return"},
                         headers={"Authorization": "Bearer pb_test_demo_key_123",
                                  "Idempotency-Key": str(uuid.uuid4())})
