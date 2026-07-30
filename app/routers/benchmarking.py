from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Company, SustainabilityPrediction, User
from ..dependencies import get_current_user

# Creating the router for benchmarking
router = APIRouter(
    prefix="/benchmarking",
    tags=["Sustainability Benchmarking"]
)

def get_benchmark_status(company_score, benchmark_score):

    difference = company_score - benchmark_score

    if difference >= 5:
        return "Above Benchmark"

    elif difference <= -5:
        return "Below Benchmark"

    else:
        return "At Benchmark"

@router.get("/company/{company_id}")
def get_company_benchmark(
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


    # 2. GET COMPANY'S LATEST ASSESSMENT

    latest = (
        db.query(SustainabilityPrediction)
        .filter(
            SustainabilityPrediction.company_id == company_id
        )
        .order_by(
            SustainabilityPrediction.prediction_date.desc()
        )
        .first()
    )

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="No sustainability assessment found for this company"
        )

    if latest.sustainability_score is None:
        raise HTTPException(
            status_code=400,
            detail="Company does not have a valid sustainability score"
        )

    company_score = float(
        latest.sustainability_score
    )


    # 3. GET LATEST SCORE FOR EVERY COMPANY


    companies = db.query(Company).all()

    benchmark_scores = []

    for benchmark_company in companies:

        prediction = (
            db.query(SustainabilityPrediction)
            .filter(
                SustainabilityPrediction.company_id
                == benchmark_company.id
            )
            .order_by(
                SustainabilityPrediction.prediction_date.desc()
            )
            .first()
        )

        if (
            prediction is not None
            and prediction.sustainability_score is not None
        ):
            benchmark_scores.append(
                {
                    "company_id": benchmark_company.id,
                    "company_name": benchmark_company.company_name,
                    "score": float(
                        prediction.sustainability_score
                    )
                }
            )


    
    # 4. CHECK BENCHMARK DATA

    if not benchmark_scores:
        raise HTTPException(
            status_code=404,
            detail="No benchmark data available"
        )


    # 5. CALCULATE MARKET BENCHMARK

    scores = [
        item["score"]
        for item in benchmark_scores
    ]

    benchmark_average = (
        sum(scores) / len(scores)
    )

    highest_score = max(scores)

    lowest_score = min(scores)

    difference = (
        company_score - benchmark_average
    )


    # 6. DETERMINE BENCHMARK STATUS

    benchmark_status = get_benchmark_status(
        company_score,
        benchmark_average
    )


    # 7. CALCULATE COMPANY RANK

    sorted_companies = sorted(
        benchmark_scores,
        key=lambda item: item["score"],
        reverse=True
    )

    company_rank = None

    for position, item in enumerate(
        sorted_companies,
        start=1
    ):

        if item["company_id"] == company_id:

            company_rank = position

            break


    # 8. GENERATE BENCHMARK INSIGHT

    if benchmark_status == "Above Benchmark":

        benchmark_insight = (
            f"{company.company_name} is performing above "
            f"the current sustainability benchmark. "
            f"The company should maintain its strong practices "
            f"while continuing to identify opportunities "
            f"for further improvement."
        )

    elif benchmark_status == "Below Benchmark":

        benchmark_insight = (
            f"{company.company_name} is currently performing "
            f"below the sustainability benchmark. "
            f"Management should review sustainability weaknesses "
            f"and prioritise improvement initiatives."
        )

    else:

        benchmark_insight = (
            f"{company.company_name} is performing close to "
            f"the current sustainability benchmark. "
            f"Further improvements could help the company "
            f"move above the benchmark."
        )


    # 9. RETURN BENCHMARK RESULTS


    return {

        "company_id": company.id,

        "company_name": company.company_name,

        "industry": company.industry,

        "country": company.country,

        "company_score": round(
            company_score,
            2
        ),

        "benchmark_average": round(
            benchmark_average,
            2
        ),

        "difference_from_benchmark": round(
            difference,
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

        "company_rank": company_rank,

        "companies_compared": len(
            benchmark_scores
        ),

        "benchmark_status":
            benchmark_status,

        "benchmark_insight":
            benchmark_insight,

        "requested_by":
            current_user.email
    }

@router.get("/company/{company_id}/industry")
def get_industry_benchmark(
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

    if not company.industry:
        raise HTTPException(
            status_code=400,
            detail="Company does not have an industry assigned"
        )



    # 2. GET COMPANY'S LATEST ASSESSMENT


    latest = (
        db.query(SustainabilityPrediction)
        .filter(
            SustainabilityPrediction.company_id == company_id
        )
        .order_by(
            SustainabilityPrediction.prediction_date.desc()
        )
        .first()
    )

    if latest is None:
        raise HTTPException(
            status_code=404,
            detail="No sustainability assessment found for this company"
        )

    if latest.sustainability_score is None:
        raise HTTPException(
            status_code=400,
            detail="Company does not have a valid sustainability score"
        )

    company_score = float(
        latest.sustainability_score
    )


    
    # 3. FIND COMPANIES IN THE SAME INDUSTRY
    

    industry_companies = (
        db.query(Company)
        .filter(
            Company.industry == company.industry
        )
        .all()
    )


    
    # 4. GET LATEST SCORE FOR EACH INDUSTRY COMPANY
    

    industry_scores = []

    for industry_company in industry_companies:

        industry_prediction = (
            db.query(SustainabilityPrediction)
            .filter(
                SustainabilityPrediction.company_id
                == industry_company.id
            )
            .order_by(
                SustainabilityPrediction.prediction_date.desc()
            )
            .first()
        )

        if (
            industry_prediction is not None
            and
            industry_prediction.sustainability_score
            is not None
        ):

            industry_scores.append(
                {
                    "company_id": industry_company.id,
                    "company_name": industry_company.company_name,
                    "score": float(
                        industry_prediction.sustainability_score
                    )
                }
            )



    # 5. CHECK INDUSTRY BENCHMARK DATA


    if not industry_scores:
        raise HTTPException(
            status_code=404,
            detail="No industry benchmark data available"
        )


    # 6. CALCULATE INDUSTRY BENCHMARK


    scores = [
        item["score"]
        for item in industry_scores
    ]

    industry_average = (
        sum(scores) / len(scores)
    )

    highest_score = max(scores)

    lowest_score = min(scores)

    difference = (
        company_score - industry_average
    )


    # 7. DETERMINE BENCHMARK STATUS


    benchmark_status = get_benchmark_status(
        company_score,
        industry_average
    )


    # 8. CALCULATE INDUSTRY RANK

    sorted_companies = sorted(
        industry_scores,
        key=lambda item: item["score"],
        reverse=True
    )

    industry_rank = None

    for position, item in enumerate(
        sorted_companies,
        start=1
    ):

        if item["company_id"] == company_id:

            industry_rank = position

            break


    # 9. CALCULATE PERCENTILE
    

    companies_below = sum(
        1
        for score in scores
        if score < company_score
    )

    industry_percentile = (
        companies_below / len(scores)
    ) * 100


    
    # 10. GENERATE INDUSTRY INSIGHT
    

    if benchmark_status == "Above Benchmark":

        industry_insight = (
            f"{company.company_name} is performing above "
            f"the current {company.industry} industry benchmark. "
            f"Its sustainability score is "
            f"{abs(difference):.2f} points above the "
            f"industry average."
        )

    elif benchmark_status == "Below Benchmark":

        industry_insight = (
            f"{company.company_name} is currently performing "
            f"below the {company.industry} industry benchmark. "
            f"Its sustainability score is "
            f"{abs(difference):.2f} points below the "
            f"industry average. Management should prioritise "
            f"the sustainability improvement areas identified "
            f"by KnowIreland AI."
        )

    else:

        industry_insight = (
            f"{company.company_name} is performing close to "
            f"the current {company.industry} industry benchmark. "
            f"Targeted sustainability improvements could help "
            f"the company move above the industry average."
        )


    
    # 11. RETURN INDUSTRY BENCHMARK
    

    return {

        "company_id": company.id,

        "company_name": company.company_name,

        "industry": company.industry,

        "country": company.country,

        "company_score": round(
            company_score,
            2
        ),

        "industry_average": round(
            industry_average,
            2
        ),

        "difference_from_industry_average": round(
            difference,
            2
        ),

        "highest_industry_score": round(
            highest_score,
            2
        ),

        "lowest_industry_score": round(
            lowest_score,
            2
        ),

        "industry_rank": industry_rank,

        "companies_compared": len(
            industry_scores
        ),

        "industry_percentile": round(
            industry_percentile,
            2
        ),

        "benchmark_status": benchmark_status,

        "industry_insight": industry_insight,

        "requested_by": current_user.email
    }