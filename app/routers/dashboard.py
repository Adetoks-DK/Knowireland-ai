from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, SustainabilityPrediction, User
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Sustainability Dashboard"]
)

# HELPER FUNCTION


def get_performance_status(score):
    """
    Convert a sustainability score into a performance category.
    """

    if score is None:
        return "Not Available"

    if score >= 80:
        return "Excellent"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Moderate"

    return "Needs Improvement"


# 1. COMPANY SUSTAINABILITY DASHBOARD

@router.get("/company/{company_id}")
def get_company_dashboard(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find company
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # Get all assessments - newest first
    predictions = (
        db.query(SustainabilityPrediction)
        .filter(
            SustainabilityPrediction.company_id == company_id
        )
        .order_by(
            SustainabilityPrediction.prediction_date.desc()
        )
        .all()
    )

    # No assessments yet
    if not predictions:
        return {
            "company_id": company.id,
            "company_name": company.company_name,
            "industry": company.industry,
            "country": company.country,
            "current_score": None,
            "previous_score": None,
            "score_change": None,
            "trend": "No previous assessment",
            "average_score": None,
            "total_assessments": 0,
            "performance_status": "Not Available",
            "latest_recommendations": None,
            "last_assessment": None,
            "message": "No sustainability assessments found.",
            "requested_by": current_user.email
        }

    # Latest assessment
    latest = predictions[0]

    current_score = (
        float(latest.sustainability_score)
        if latest.sustainability_score is not None
        else None
    )

    
    # Previous score and score change


    previous_score = None
    score_change = None

    if (
        len(predictions) > 1
        and predictions[1].sustainability_score is not None
    ):
        previous_score = float(
            predictions[1].sustainability_score
        )

        if current_score is not None:
            score_change = current_score - previous_score

    # Trend

    if score_change is None:
        trend = "No previous assessment"

    elif score_change > 0:
        trend = "Improving"

    elif score_change < 0:
        trend = "Declining"

    else:
        trend = "No change"

    # Average score

    valid_scores = [
        float(item.sustainability_score)
        for item in predictions
        if item.sustainability_score is not None
    ]

    average_score = (
        sum(valid_scores) / len(valid_scores)
        if valid_scores
        else None
    )

    # Performance status
    performance_status = get_performance_status(
        current_score
    )

    return {
        "company_id": company.id,
        "company_name": company.company_name,
        "industry": company.industry,
        "country": company.country,

        "current_score": (
            round(current_score, 2)
            if current_score is not None
            else None
        ),

        "previous_score": (
            round(previous_score, 2)
            if previous_score is not None
            else None
        ),

        "score_change": (
            round(score_change, 2)
            if score_change is not None
            else None
        ),

        "trend": trend,

        "average_score": (
            round(average_score, 2)
            if average_score is not None
            else None
        ),

        "total_assessments": len(predictions),

        "performance_status": performance_status,

        "latest_recommendations":
            latest.recommendations,

        "last_assessment":
            latest.prediction_date,

        "requested_by":
            current_user.email
    }


# 2. SUSTAINABILITY ASSESSMENT HISTORY

@router.get("/company/{company_id}/history")
def get_prediction_history(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find company
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # Get assessments - oldest first
    predictions = (
        db.query(SustainabilityPrediction)
        .filter(
            SustainabilityPrediction.company_id == company_id
        )
        .order_by(
            SustainabilityPrediction.prediction_date.asc()
        )
        .all()
    )

    history = []

    for prediction in predictions:

        score = (
            float(prediction.sustainability_score)
            if prediction.sustainability_score is not None
            else None
        )

        performance_status = get_performance_status(
            score
        )

        history.append({
            "prediction_id": prediction.id,

            "score": (
                round(score, 2)
                if score is not None
                else None
            ),

            "performance_status":
                performance_status,

            "recommendations":
                prediction.recommendations,

            "date":
                prediction.prediction_date
        })

    return {
        "company_id": company.id,
        "company_name": company.company_name,
        "total_assessments": len(history),
        "history": history,
        "requested_by": current_user.email
    }



# 3. LATEST SUSTAINABILITY ASSESSMENT


@router.get("/company/{company_id}/latest")
def get_latest_prediction(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Find company
    company = (
        db.query(Company)
        .filter(Company.id == company_id)
        .first()
    )

    if company is None:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    # Get the two most recent assessments
    predictions = (
        db.query(SustainabilityPrediction)
        .filter(
            SustainabilityPrediction.company_id == company_id
        )
        .order_by(
            SustainabilityPrediction.prediction_date.desc()
        )
        .limit(2)
        .all()
    )

    if not predictions:
        raise HTTPException(
            status_code=404,
            detail="No sustainability assessment found for this company"
        )

    # Latest prediction
    latest = predictions[0]

    score = (
        float(latest.sustainability_score)
        if latest.sustainability_score is not None
        else None
    )

    
    # Previous score
    

    previous_score = None
    score_change = None

    if (
        len(predictions) > 1
        and predictions[1].sustainability_score is not None
    ):

        previous_score = float(
            predictions[1].sustainability_score
        )

        if score is not None:
            score_change = score - previous_score

    
    # Determine trend
    

    if score_change is None:
        trend = "No previous assessment"

    elif score_change > 0:
        trend = "Improving"

    elif score_change < 0:
        trend = "Declining"

    else:
        trend = "No change"

    
    # Performance status
    

    performance_status = get_performance_status(
        score
    )


    # Return latest assessment

    return {
        "prediction_id": latest.id,

        "company_id": company.id,

        "company_name": company.company_name,

        "sustainability_score": (
            round(score, 2)
            if score is not None
            else None
        ),

        "previous_score": (
            round(previous_score, 2)
            if previous_score is not None
            else None
        ),

        "score_change": (
            round(score_change, 2)
            if score_change is not None
            else None
        ),

        "trend": trend,

        "performance_status":
            performance_status,

        "recommendations":
            latest.recommendations,

        "energy_consumption":
            latest.energy_consumption,

        "water_consumption":
            latest.water_consumption,

        "waste_generated":
            latest.waste_generated,

        "recycling_rate":
            latest.recycling_rate,

        "renewable_energy":
            latest.renewable_energy,

        "transport_emissions":
            latest.transport_emissions,

        "carbon_emissions":
            latest.carbon_emissions,

        "prediction_date":
            latest.prediction_date,

        "requested_by":
            current_user.email
    }