from pydantic import BaseModel, Field


class QuoteRequest(BaseModel):
    material_name: str = Field(default="PLA")
    filament_spool_price: float = Field(gt=0, examples=[90.0])
    filament_spool_weight_g: float = Field(gt=0, examples=[1000.0])
    part_weight_g: float = Field(gt=0, examples=[42.0])
    print_hours: float = Field(gt=0, examples=[4.5])
    printer_power_w: float = Field(gt=0, examples=[120.0])
    electricity_price_kwh: float = Field(ge=0, examples=[0.95])
    printer_price: float = Field(gt=0, examples=[2800.0])
    printer_lifetime_hours: float = Field(gt=0, examples=[3500.0])
    maintenance_cost_per_hour: float = Field(ge=0, default=0.0)
    labor_minutes: float = Field(ge=0, default=0.0)
    labor_hour_price: float = Field(ge=0, default=0.0)
    packaging_cost: float = Field(ge=0, default=0.0)
    failure_rate_percent: float = Field(ge=0, le=100, default=8.0)
    profit_margin_percent: float = Field(ge=0, default=35.0)
    marketplace_fee_percent: float = Field(ge=0, lt=100, default=0.0)
    quantity: int = Field(ge=1, default=1)


class QuoteBreakdown(BaseModel):
    material_cost: float
    energy_cost: float
    depreciation_cost: float
    maintenance_cost: float
    labor_cost: float
    packaging_cost: float
    base_cost: float
    failure_buffer: float
    cost_with_buffer: float
    profit_value: float
    marketplace_fee_value: float
    unit_price: float
    total_price: float


class QuoteResponse(BaseModel):
    material_name: str
    quantity: int
    currency: str = "BRL"
    breakdown: QuoteBreakdown
