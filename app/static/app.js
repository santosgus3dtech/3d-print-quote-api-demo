const currency = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });
const labels = {
  material_cost: "Material", energy_cost: "Energy", depreciation_cost: "Depreciation",
  maintenance_cost: "Maintenance", labor_cost: "Labor", packaging_cost: "Packaging",
  failure_buffer: "Failure buffer", profit_value: "Profit", marketplace_fee_value: "Marketplace fee",
};

document.querySelector("#quote-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = Object.fromEntries(new FormData(event.currentTarget));
  for (const key of Object.keys(payload)) if (key !== "material_name") payload[key] = Number(payload[key]);
  const response = await fetch("/quote", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) });
  if (!response.ok) { document.querySelector("#unit").textContent = "Review the highlighted inputs."; return; }
  const quote = await response.json();
  document.querySelector("#total").textContent = currency.format(quote.breakdown.total_price);
  document.querySelector("#unit").textContent = `${quote.quantity} units · ${currency.format(quote.breakdown.unit_price)} each · ${quote.material_name}`;
  document.querySelector("#breakdown").innerHTML = Object.entries(labels).map(([key, label]) => `<div><span>${label}</span><strong>${currency.format(quote.breakdown[key])}</strong></div>`).join("");
});
document.querySelector("#quote-form").requestSubmit();
