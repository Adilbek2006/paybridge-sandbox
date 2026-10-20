"""API-key authentication (FR-01, FR-02). Owner: Adilbek.

Prototype: keys come from the PAYBRIDGE_API_KEYS env var ("key:merchant_id,...").
The production version stores SHA-256 hashes in the api_keys table.
"""
import hashlib
import hmac
import os

from fastapi import Header, HTTPException


def _load_keys() -> dict[str, str]:
    raw = os.getenv("PAYBRIDGE_API_KEYS", "pb_test_demo_key_123:merch_demo")
    pairs = (item.split(":", 1) for item in raw.split(",") if ":" in item)
    return {hashlib.sha256(k.encode()).hexdigest(): m for k, m in pairs}


_KEY_HASHES = _load_keys()


def current_merchant(authorization: str | None = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid API key")
    digest = hashlib.sha256(authorization[7:].encode()).hexdigest()
    for stored, merchant in _KEY_HASHES.items():
        if hmac.compare_digest(stored, digest):
            return merchant
    raise HTTPException(status_code=401, detail="Missing or invalid API key")
