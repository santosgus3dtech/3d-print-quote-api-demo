from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .models import QuoteRequest, QuoteResponse
from .pricing import calculate_quote


app = FastAPI(
    title="3D Print Quote API Demo",
    version="0.1.0",
    description="Sanitized demo API for estimating 3D-printing quotes from fake input data.",
)

STATIC_DIR = Path(__file__).resolve().parent / "static"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/quote", response_model=QuoteResponse)
def quote(data: QuoteRequest) -> QuoteResponse:
    return calculate_quote(data)


app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")


@app.get("/", include_in_schema=False)
def calculator() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
