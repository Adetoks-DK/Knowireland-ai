from app.prediction_service import predict_sustainability
low_company = {
    "employees": 100,
    "annual_revenue": 5000000,
    "energy_consumption": 900,
    "water_consumption": 900,
    "waste_generated": 900,
    "recycling_rate": 10,
    "renewable_energy": 5,
    "transport_emissions": 900,
    "carbon_emissions": 900
}

medium_company = {
    "employees": 100,
    "annual_revenue": 5000000,
    "energy_consumption": 500,
    "water_consumption": 500,
    "waste_generated": 450,
    "recycling_rate": 50,
    "renewable_energy": 50,
    "transport_emissions": 450,
    "carbon_emissions": 450
}

high_company = {
    "employees": 100,
    "annual_revenue": 5000000,
    "energy_consumption": 150,
    "water_consumption": 150,
    "waste_generated": 100,
    "recycling_rate": 90,
    "renewable_energy": 90,
    "transport_emissions": 100,
    "carbon_emissions": 100
}

print(
    "Low:",
    predict_sustainability(low_company)
)

print(
    "Medium:",
    predict_sustainability(medium_company)
)

print(
    "High:",
    predict_sustainability(high_company)
)