"""Idempotency store (FR-08). Owner: Adilbek.

Prototype keeps keys in memory guarded by a lock. The production version uses the
`idempotency_keys` table with a unique (merchant_id, key) constraint (ADR-002).
"""
import hashlib
import json
import threading
from dataclasses import dataclass, field


@dataclass
class StoredResponse:
    request_hash: str
    status_code: int | None = None
    body: dict | None = None
    done: threading.Event = field(default_factory=threading.Event)


class IdempotencyConflict(Exception):
    """Same key reused with a different request body."""


class IdempotencyStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._items: dict[tuple[str, str, str], StoredResponse] = {}

    @staticmethod
    def hash_request(body: dict) -> str:
        return hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()

    def reserve(self, merchant_id: str, endpoint: str, key: str, request_hash: str) -> tuple[bool, StoredResponse]:
        """Returns (is_new, entry). Only the first caller gets is_new=True."""
        with self._lock:
            entry = self._items.get((merchant_id, endpoint, key))
            if entry is None:
                entry = StoredResponse(request_hash=request_hash)
                self._items[(merchant_id, endpoint, key)] = entry
                return True, entry
        if entry.request_hash != request_hash:
            raise IdempotencyConflict()
        entry.done.wait(timeout=30)
        return False, entry

    def complete(self, entry: StoredResponse, status_code: int, body: dict) -> None:
        entry.status_code, entry.body = status_code, body
        entry.done.set()
