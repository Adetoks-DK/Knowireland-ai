def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(value, maximum))


def calculate_sustainability_score(data):

    
    # Renewable energy

    renewable_score = clamp(
        data.renewable_energy
    )

    
    # Recycling
    
    recycling_score = clamp(
        data.recycling_rate
    )

    
    # Carbon emissions
    # Lower emissions = better
    
    carbon_score = clamp(
        100 - (data.carbon_emissions / 10)
    )

    
    # Energy consumption
    # Lower consumption = better
    
    energy_score = clamp(
        100 - (data.energy_consumption / 100)
    )

    
    # Water consumption
    
    water_score = clamp(
        100 - (data.water_consumption / 100)
    )

    
    # Waste generation
    
    waste_score = clamp(
        100 - (data.waste_generated / 10)
    )

    
    # Transport emissions
    
    transport_score = clamp(
        100 - (data.transport_emissions / 10)
    )

    
    # Weighted final score
    

    final_score = (
        carbon_score * 0.25
        + renewable_score * 0.20
        + recycling_score * 0.15
        + waste_score * 0.15
        + energy_score * 0.10
        + water_score * 0.10
        + transport_score * 0.05
    )

    return {
        "overall_score": round(final_score, 2),
        "carbon_score": round(carbon_score, 2),
        "renewable_score": round(renewable_score, 2),
        "recycling_score": round(recycling_score, 2),
        "waste_score": round(waste_score, 2),
        "energy_score": round(energy_score, 2),
        "water_score": round(water_score, 2),
        "transport_score": round(transport_score, 2)
    }

def get_sustainability_rating(score):

    if score >= 80:
        return "Leading"

    elif score >= 65:
        return "Strong"

    elif score >= 50:
        return "Developing"

    elif score >= 35:
        return "Needs Improvement"

    else:
        return "High Priority"
    

    
