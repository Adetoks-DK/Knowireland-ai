from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Company, SustainabilityPrediction
from app.schemas import SustainabilityInput
from app.sustainability_scoring import calculate_sustainability_score
from app.recommendation_engine import generate_recommendations

router = APIRouter(
    prefix="/prediction",
    tags=["Sustainability Prediction"]
)


@router.post("/{company_id}")
def create_prediction(
    company_id: int,
    data: SustainabilityInput,
    db: Session = Depends(get_db)
):
    """
    Create a sustainability assessment for a company.
    """

    # Check that the company exists
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found."
        )

    # Convert request to dictionary
    input_data = data.model_dump()

    # Calculate sustainability scores
    scores = calculate_sustainability_score(input_data)

    prediction_score = scores.get("overall_score", 0)

    # Generate recommendations
    recommendation_list = generate_recommendations(scores)

    recommendation_text = " | ".join(recommendation_list)

    # Create prediction record
    prediction = SustainabilityPrediction(
        company_id=company.id,
        energy_consumption=data.energy_consumption,
        water_consumption=data.water_consumption,
        waste_generated=data.waste_generated,
        recycling_rate=data.recycling_rate,
        renewable_energy=data.renewable_energy,
        transport_emissions=data.transport_emissions,
        carbon_emissions=data.carbon_emissions,
        sustainability_score=prediction_score,
        recommendations=recommendation_text
    )

    # Save prediction
    try:
        db.add(prediction)
        db.commit()
        db.refresh(prediction)

    except Exception as e:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

    # Return response
    return {
        "message": "Sustainability assessment completed successfully.",

        "prediction_id": prediction.id,

        "company": {
            "id": company.id,
            "name": company.company_name
        },

        "overall_score": round(prediction_score, 2),

        "category_scores": {
            "carbon": scores.get("carbon_score"),
            "energy": scores.get("energy_score"),
            "water": scores.get("water_score"),
            "waste": scores.get("waste_score"),
            "recycling": scores.get("recycling_score"),
            "renewable_energy": scores.get("renewable_score"),
            "transport": scores.get("transport_score")
        },

        "recommendations": recommendation_list
    }
