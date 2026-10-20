"""PayBridge API — probation-period prototype (in-memory storage, mock provider)."""
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .api.deps import current_merchant
from .api.errors import problem
from .domain.models import CreatePaymentRequest, RefundRequest
from .domain.state_machine import InvalidTransition
from .providers.base import ProviderError
from .services.idempotency import IdempotencyConflict, IdempotencyStore
from .services.payments import PaymentNotFound, PaymentService, RefundTooLarge

app = FastAPI(title="PayBridge Sandbox API", version="0.1.0")
payments = PaymentService()
idempotency = IdempotencyStore()


@app.exception_handler(HTTPException)
async def http_error(_: Request, exc: HTTPException):
    return problem(exc.status_code, "Unauthorized" if exc.status_code == 401 else "Error", str(exc.detail), "http")


@app.exception_handler(RequestValidationError)
async def validation_error(_: Request, exc: RequestValidationError):
    return problem(422, "Validation error", str(exc.errors()[0].get("msg")), "validation")


def _run_idempotent(merchant: str, endpoint: str, key: str | None, body: dict, action) -> JSONResponse:
    if not key or not (8 <= len(key) <= 255):
        return problem(422, "Idempotency-Key required", "Send an Idempotency-Key header (8-255 chars)", "idempotency-key-required")
    try:
        is_new, entry = idempotency.reserve(merchant, endpoint, key, idempotency.hash_request(body))
    except IdempotencyConflict:
        return problem(422, "Idempotency key reused with different parameters",
                       f"The key '{key[:8]}…' was used for a request with a different body", "idempotency-key-reused")
    if not is_new:
        return _json(entry.status_code, entry.body)
    try:
        status, content = action()
    except PaymentNotFound:
        status, content = 404, _err(404, "Not found", "Payment not found", "not-found")
    except InvalidTransition as exc:
        status, content = 409, _err(409, "Invalid state transition", str(exc), "invalid-transition")
    except RefundTooLarge as exc:
        status, content = 422, _err(422, "Refund exceeds refundable amount", str(exc), "refund-too-large")
    except ProviderError as exc:
        status, content = 502, _err(502, "Provider error", str(exc), "provider-error")
    except ValueError as exc:
        status, content = 422, _err(422, "Unsupported provider", str(exc), "unsupported-provider")
    idempotency.complete(entry, status, content)
    return _json(status, content)


def _err(status: int, title: str, detail: str, slug: str) -> dict:
    return {"type": f"https://paybridge.dev/errors/{slug}", "title": title, "status": status, "detail": detail}


def _json(status: int, content: dict) -> JSONResponse:
    media = "application/problem+json" if status >= 400 else "application/json"
    return JSONResponse(status_code=status, content=content, media_type=media)


@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}


@app.post("/v1/payments", status_code=201, tags=["Payments"])
def create_payment(req: CreatePaymentRequest, merchant: str = Depends(current_merchant),
                   idempotency_key: str | None = Header(default=None)):
    def action():
        p = payments.create(merchant, req)
        return 201, p.model_dump(mode="json", exclude={"merchant_id", "status_history"})
    return _run_idempotent(merchant, "create_payment", idempotency_key, req.model_dump(mode="json"), action)


@app.get("/v1/payments", tags=["Payments"])
def list_payments(merchant: str = Depends(current_merchant)):
    data = [p.model_dump(mode="json", exclude={"merchant_id", "status_history"}) for p in payments.list(merchant)]
    return {"data": data, "next_cursor": None}


@app.get("/v1/payments/{payment_id}", tags=["Payments"])
def get_payment(payment_id: str, merchant: str = Depends(current_merchant)):
    try:
        return payments.get(merchant, payment_id).model_dump(mode="json", exclude={"merchant_id"})
    except PaymentNotFound:
        return problem(404, "Not found", f"Payment {payment_id} not found", "not-found")


@app.post("/v1/payments/{payment_id}/cancel", tags=["Payments"])
def cancel_payment(payment_id: str, merchant: str = Depends(current_merchant),
                   idempotency_key: str | None = Header(default=None)):
    def action():
        return 200, payments.cancel(merchant, payment_id).model_dump(mode="json", exclude={"merchant_id", "status_history"})
    return _run_idempotent(merchant, f"cancel:{payment_id}", idempotency_key, {}, action)


@app.post("/v1/payments/{payment_id}/refunds", status_code=201, tags=["Refunds"])
def refund_payment(payment_id: str, req: RefundRequest, merchant: str = Depends(current_merchant),
                   idempotency_key: str | None = Header(default=None)):
    def action():
        p = payments.refund(merchant, payment_id, req.amount)
        return 201, {"payment_id": p.id, "status": p.status.value, "amount_refunded": p.amount_refunded}
    return _run_idempotent(merchant, f"refund:{payment_id}", idempotency_key, req.model_dump(mode="json"), action)
