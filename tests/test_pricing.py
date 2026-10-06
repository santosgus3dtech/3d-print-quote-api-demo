from fastapi.testclient import TestClient

from app.main import app
from app.models import QuoteRequest
from app.pricing import calculate_quote


client = TestClient(app)


def test_calculate_quote_breakdown_is_stable():
    quote = calculate_quote(
        QuoteRequest(
            material_name="PLA",
            filament_spool_price=100,
            filament_spool_weight_g=1000,
            part_weight_g=50,
            print_hours=5,
            printer_power_w=100,
            electricity_price_kwh=1,
            printer_price=2500,
            printer_lifetime_hours=2500,
            maintenance_cost_per_hour=0.5,
            labor_minutes=30,
            labor_hour_price=30,
            packaging_cost=4,
            failure_rate_percent=10,
            profit_margin_percent=40,
            marketplace_fee_percent=20,
            quantity=2,
        )
    )

    assert quote.breakdown.material_cost == 5
    assert quote.breakdown.energy_cost == 0.5
    assert quote.breakdown.depreciation_cost == 5
    assert quote.breakdown.unit_price == 61.6
    assert quote.breakdown.total_price == 123.2


def test_quote_endpoint_returns_response_model():
    response = client.post(
        "/quote",
        json={
            "material_name": "PETG",
            "filament_spool_price": 110,
            "filament_spool_weight_g": 1000,
            "part_weight_g": 32,
            "print_hours": 3.5,
            "printer_power_w": 130,
            "electricity_price_kwh": 0.9,
            "printer_price": 2800,
            "printer_lifetime_hours": 3500,
            "quantity": 3,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["material_name"] == "PETG"
    assert payload["quantity"] == 3
    assert payload["breakdown"]["unit_price"] > 0


def test_invalid_marketplace_fee_is_rejected():
    response = client.post(
        "/quote",
        json={
            "filament_spool_price": 90,
            "filament_spool_weight_g": 1000,
            "part_weight_g": 20,
            "print_hours": 2,
            "printer_power_w": 100,
            "electricity_price_kwh": 1,
            "printer_price": 2000,
            "printer_lifetime_hours": 3000,
            "marketplace_fee_percent": 100,
        },
    )

    assert response.status_code == 422


def test_calculator_is_the_default_experience():
    response = client.get("/")
    assert response.status_code == 200
    assert "3D print cost calculator" in response.text
