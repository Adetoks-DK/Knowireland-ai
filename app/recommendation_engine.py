def generate_recommendations(scores):

    recommendations = []

    if scores["carbon_score"] < 60:
        recommendations.append(
            "Develop a carbon reduction plan and identify "
            "the company's largest sources of emissions."
        )

    if scores["renewable_score"] < 60:
        recommendations.append(
            "Increase the proportion of energy obtained "
            "from renewable sources."
        )

    if scores["recycling_score"] < 60:
        recommendations.append(
            "Improve waste segregation and recycling practices."
        )

    if scores["waste_score"] < 60:
        recommendations.append(
            "Introduce waste reduction and circular economy initiatives."
        )

    if scores["energy_score"] < 60:
        recommendations.append(
            "Conduct an energy efficiency review and identify "
            "opportunities to reduce energy consumption."
        )

    if scores["water_score"] < 60:
        recommendations.append(
            "Review water consumption and introduce water-saving measures."
        )

    if scores["transport_score"] < 60:
        recommendations.append(
            "Explore lower-emission transport, route optimisation "
            "and electric vehicle opportunities."
        )

    if not recommendations:
        recommendations.append(
            "Sustainability performance is strong across the assessed "
            "categories. Continue monitoring performance and set "
            "progressive improvement targets."
        )

    return recommendations