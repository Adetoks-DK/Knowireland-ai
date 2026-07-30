from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, SustainabilityPrediction
from ..schemas import SustainabilityInput

from ..sustainability_scoring import calculate_sustainability_score
from ..recommendation_engine import generate_recommendations

from ..security import get_current_user
from ..models import User

from ..dependencies import get_current_user
from ..models import User


router = APIRouter(
    prefix="/prediction",
    tags=["Sustainability Prediction"]
)


@router.post("/{company_id}")
def create_prediction(
    company_id: int,
    data: SustainabilityInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # STEP 1: Find the company


    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )


    # STEP 2: Calculate sustainability scores

    scores = calculate_sustainability_score(data)

    prediction_score = scores["overall_score"]

    recommendation_list = generate_recommendations(scores)

    recommendation = " | ".join(recommendation_list)


    # STEP 3: Create prediction database record

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
        recommendations=recommendation
    )

    # STEP 4: Save prediction to MySQL

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

    # STEP 5: Return result

    return {
        "message": "Sustainability assessment completed successfully",

        "prediction_id": prediction.id,

        "company": {
            "id": company.id,
            "name": company.company_name
        },

        "overall_score": prediction_score,

        "category_scores": {
            "carbon": scores["carbon_score"],
            "renewable_energy": scores["renewable_score"],
            "recycling": scores["recycling_score"],
            "waste": scores["waste_score"],
            "energy": scores["energy_score"],
            "water": scores["water_score"],
            "transport": scores["transport_score"]
        },

        "recommendations": recommendation_list
    }

    return {
    "message": "Prediction completed and saved successfully",
    "prediction_id": prediction.id,
    "company_id": company.id,
    "company_name": company.company_name,
    "sustainability_score": prediction.sustainability_score,
    "recommendations": prediction.recommendations,
    "generated_by": current_user.email
}