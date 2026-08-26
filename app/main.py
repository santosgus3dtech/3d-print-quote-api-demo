from fastapi import FastAPI

from .models import QuoteRequest, QuoteResponse
from .pricing import calculate_quote


app = FastAPI(
    title="3D Print Quote API Demo",
    version="0.1.0",
    description="Sanitized demo API for estimating 3D-printing quotes from fake input data.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/quote", response_model=QuoteResponse)
def quote(data: QuoteRequest) -> QuoteResponse:
    return calculate_quote(data)
