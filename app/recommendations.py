def generate_recommendations(data):

    recommendations=[]

    if data["recycling_rate"]<60:

        recommendations.append(
            "Increase recycling programmes."
        )

    if data["renewable_energy"]<40:

        recommendations.append(
            "Increase renewable energy usage."
        )

    if data["carbon_emissions"]>250:

        recommendations.append(
            "Reduce carbon emissions."
        )

    if data["transport_emissions"]>200:

        recommendations.append(
            "Introduce greener transportation."
        )

    if len(recommendations)==0:

        recommendations.append(
            "Excellent sustainability performance."
        )

    return recommendations