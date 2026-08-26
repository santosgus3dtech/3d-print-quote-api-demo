from .models import QuoteBreakdown, QuoteRequest, QuoteResponse


def round_money(value: float) -> float:
    return round(value + 1e-9, 2)


def calculate_quote(data: QuoteRequest) -> QuoteResponse:
    gram_price = data.filament_spool_price / data.filament_spool_weight_g
    material_cost = data.part_weight_g * gram_price
    energy_cost = (data.printer_power_w / 1000) * data.print_hours * data.electricity_price_kwh
    depreciation_cost = (data.printer_price / data.printer_lifetime_hours) * data.print_hours
    maintenance_cost = data.maintenance_cost_per_hour * data.print_hours
    labor_cost = (data.labor_minutes / 60) * data.labor_hour_price

    base_cost = (
        material_cost
        + energy_cost
        + depreciation_cost
        + maintenance_cost
        + labor_cost
        + data.packaging_cost
    )
    failure_buffer = base_cost * (data.failure_rate_percent / 100)
    cost_with_buffer = base_cost + failure_buffer
    profit_value = cost_with_buffer * (data.profit_margin_percent / 100)
    price_before_marketplace = cost_with_buffer + profit_value

    if data.marketplace_fee_percent:
        unit_price = price_before_marketplace / (1 - data.marketplace_fee_percent / 100)
    else:
        unit_price = price_before_marketplace

    marketplace_fee_value = unit_price - price_before_marketplace
    total_price = unit_price * data.quantity

    return QuoteResponse(
        material_name=data.material_name,
        quantity=data.quantity,
        breakdown=QuoteBreakdown(
            material_cost=round_money(material_cost),
            energy_cost=round_money(energy_cost),
            depreciation_cost=round_money(depreciation_cost),
            maintenance_cost=round_money(maintenance_cost),
            labor_cost=round_money(labor_cost),
            packaging_cost=round_money(data.packaging_cost),
            base_cost=round_money(base_cost),
            failure_buffer=round_money(failure_buffer),
            cost_with_buffer=round_money(cost_with_buffer),
            profit_value=round_money(profit_value),
            marketplace_fee_value=round_money(marketplace_fee_value),
            unit_price=round_money(unit_price),
            total_price=round_money(total_price),
        ),
    )
