"""RFC 9457 problem responses."""
from fastapi.responses import JSONResponse


def problem(status: int, title: str, detail: str, slug: str) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        media_type="application/problem+json",
        content={"type": f"https://paybridge.dev/errors/{slug}", "title": title, "status": status, "detail": detail},
    )
