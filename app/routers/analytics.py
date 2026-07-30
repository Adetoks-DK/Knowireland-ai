from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, SustainabilityPrediction, User
from ..dependencies import get_current_user


router = APIRouter(
    prefix="/analytics",
    tags=["Sustainability Analytics"]
)



# PERFORMANCE STATUS HELPER


def get_performance_status(score):

    if score is None:
        return "Not Available"

    elif score >= 80:
        return "Excellent"

    elif score >= 60:
        return "Good"

    elif score >= 40:
        return "Moderate"

    else:
        return "Needs Improvement"



# COMPANY SUSTAINABILITY ANALYTICS


@router.get("/company/{company_id}")
def get_company_analytics(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    
    # 1. FIND COMPANY
    

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


    
    # 2. GET ALL SUSTAINABILITY ASSESSMENTS
    

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

    if not predictions:
        return {
            "company_id": company.id,
            "company_name": company.company_name,
            "total_assessments": 0,
            "message": "No sustainability assessments found.",
            "requested_by": current_user.email
        }


    
    # 3. EXTRACT VALID SCORES
    

    scores = [
        float(item.sustainability_score)
        for item in predictions
        if item.sustainability_score is not None
    ]

    if not scores:
        return {
            "company_id": company.id,
            "company_name": company.company_name,
            "total_assessments": len(predictions),
            "message": "No valid sustainability scores found.",
            "requested_by": current_user.email
        }


    
    # 4. CALCULATE ANALYTICS
    

    first_score = scores[0]

    current_score = scores[-1]

    average_score = sum(scores) / len(scores)

    highest_score = max(scores)

    lowest_score = min(scores)

    improvement = current_score - first_score


    
    # 5. DETERMINE TREND
    

    if len(scores) < 2:

        trend = "No previous assessment"

    elif current_score > scores[-2]:

        trend = "Improving"

    elif current_score < scores[-2]:

        trend = "Declining"

    else:

        trend = "No change"


    
    # 6. PERFORMANCE STATUS
    

    performance_status = get_performance_status(
        current_score
    )


    # 7. GET LATEST ASSESSMENT
    

    latest = predictions[-1]


    
    # 8. IDENTIFY STRENGTHS AND IMPROVEMENT AREAS
    

    strengths = []

    improvement_areas = []


    # Recycling performance

    if (
        latest.recycling_rate is not None
        and latest.recycling_rate >= 70
    ):

        strengths.append(
            "Strong recycling performance"
        )

    else:

        improvement_areas.append(
            "Increase recycling rate"
        )


    # Renewable energy performance

    if (
        latest.renewable_energy is not None
        and latest.renewable_energy >= 60
    ):

        strengths.append(
            "Strong use of renewable energy"
        )

    else:

        improvement_areas.append(
            "Increase renewable energy usage"
        )


    # Overall sustainability performance

    if current_score >= 80:

        strengths.append(
            "Strong overall sustainability performance"
        )

    elif current_score < 60:

        improvement_areas.append(
            "Improve overall sustainability performance"
        )


    
    # 9. EXECUTIVE SUMMARY
    

    if trend == "Improving":

        executive_summary = (
            f"{company.company_name} is showing an improving "
            f"sustainability trend with a current score of "
            f"{current_score:.2f}. "
            f"The organisation should continue its current "
            f"improvement programme while focusing on the "
            f"identified improvement areas."
        )

    elif trend == "Declining":

        executive_summary = (
            f"{company.company_name} has experienced a decline "
            f"in its latest sustainability performance. "
            f"Management should review the identified "
            f"improvement areas and prioritise corrective action."
        )

    elif trend == "No change":

        executive_summary = (
            f"{company.company_name} has maintained its "
            f"sustainability performance with a current score "
            f"of {current_score:.2f}. "
            f"Continued monitoring and improvement are recommended."
        )

    else:

        executive_summary = (
            f"{company.company_name} currently has a "
            f"sustainability score of {current_score:.2f}. "
            f"Further assessments are required to establish "
            f"a sustainability performance trend."
        )


    
    # 10. RETURN ANALYTICS
    

    return {

        "company_id": company.id,

        "company_name": company.company_name,

        "industry": company.industry,

        "country": company.country,

        "total_assessments": len(predictions),

        "current_score": round(
            current_score,
            2
        ),

        "first_score": round(
            first_score,
            2
        ),

        "average_score": round(
            average_score,
            2
        ),

        "highest_score": round(
            highest_score,
            2
        ),

        "lowest_score": round(
            lowest_score,
            2
        ),

        "improvement_from_first_assessment": round(
            improvement,
            2
        ),

        "trend": trend,

        "performance_status": performance_status,

        "strengths": strengths,

        "improvement_areas": improvement_areas,

        "executive_summary": executive_summary,

        "requested_by": current_user.email
    }