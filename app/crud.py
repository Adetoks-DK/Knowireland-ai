from .models import Company


def create_company(db, company):

    new_company = Company(

        company_name=company.company_name,

        industry=company.industry,

        employees=company.employees,

        annual_revenue=company.annual_revenue,

        country=company.country

    )

    db.add(new_company)

    db.commit()

    db.refresh(new_company)

    return new_company

from .models import SustainabilityPrediction

def save_prediction(db,data):

    prediction=SustainabilityPrediction(**data)

    db.add(prediction)

    db.commit()

    db.refresh(prediction)

    return prediction