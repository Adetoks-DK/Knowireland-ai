{
  "company_name":"ABC Manufacturing",

  "industry":"Manufacturing",

  "employees":180,

  "annual_revenue":8500000,

  "country":"Ireland"
}
from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CompanyCreate
from ..crud import create_company

router = APIRouter()


@router.post("/company")
def register_company(

    company: CompanyCreate,

    db: Session = Depends(get_db)

):

    return create_company(db, company)