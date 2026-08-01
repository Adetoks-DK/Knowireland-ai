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

    scores = calculate_sustainability_score(data.model_dump())

    recommendation_list = generate_recommendations(scores)

    prediction = SustainabilityPrediction(
        company_id=company.id,
        energy_consumption=data.energy_consumption,
        water_consumption=data.water_consumption,
        waste_generated=data.waste_generated,
        recycling_rate=data.recycling_rate,
        renewable_energy=data.renewable_energy,
        transport_emissions=data.transport_emissions,
        carbon_emissions=data.carbon_emissions,
        sustainability_score=scores["overall_score"],
        recommendations=" | ".join(recommendation_list)
    )

    db.add(prediction)
    db.commit()
    db.refresh(prediction)

    return {
        "message": "Prediction completed successfully",
        "prediction_id": prediction.id,
        "company_id": company.id,
        "company_name": company.company_name,
        "overall_score": scores["overall_score"],
        "category_scores": scores,
        "recommendations": recommendation_list
    }


@router.post("/public")
def public_prediction(data: SustainabilityInput):
    """
    Public endpoint for Streamlit and KnowIreland.ie.
    """

    scores = calculate_sustainability_score(data.model_dump())

    recommendations = generate_recommendations(scores)

    return {
        "overall_score": scores["overall_score"],
        "category_scores": scores,
        "recommendations": recommendations
    }