import streamlit as st
import requests

API = "https://knowireland-ai-2.onrender.com"

st.title("🌱 KnowIreland AI")

with st.form("assessment"):

    employees = st.number_input("Employees", value=50)

    annual_revenue = st.number_input(
        "Annual Revenue",
        value=1000000.0
    )

    energy_consumption = st.number_input(
        "Energy Consumption",
        value=50000.0
    )

    water_consumption = st.number_input(
        "Water Consumption",
        value=12000.0
    )

    waste_generated = st.number_input(
        "Waste Generated",
        value=2500.0
    )

    recycling_rate = st.slider(
        "Recycling Rate",
        0,
        100,
        60
    )

    renewable_energy = st.slider(
        "Renewable Energy",
        0,
        100,
        35
    )

    transport_emissions = st.number_input(
        "Transport Emissions",
        value=1200.0
    )

    carbon_emissions = st.number_input(
        "Carbon Emissions",
        value=5200.0
    )

    submit = st.form_submit_button(
        "Predict"
    )

if submit:

    payload = {
        "employees": employees,
        "annual_revenue": annual_revenue,
        "energy_consumption": energy_consumption,
        "water_consumption": water_consumption,
        "waste_generated": waste_generated,
        "recycling_rate": recycling_rate,
        "renewable_energy": renewable_energy,
        "transport_emissions": transport_emissions,
        "carbon_emissions": carbon_emissions
    }

    response = requests.post(
        f"{API}/prediction/public",
        json=payload,
        timeout=60
    )

    if response.status_code == 200:

        result = response.json()

        score = result["overall_score"]

        st.metric(
            "Overall Sustainability Score",
            f"{score:.2f}/100"
        )

        st.progress(score / 100)

        st.subheader("Recommendations")

        for item in result["recommendations"]:
            st.write("✅", item)

    else:
        st.error(response.text)