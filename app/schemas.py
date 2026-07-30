from pydantic import BaseModel, EmailStr, Field

# SUSTAINABILITY SCHEMAS


class SustainabilityInput(BaseModel):
    employees: int = Field(gt=0)
    annual_revenue: float = Field(ge=0)
    energy_consumption: float = Field(ge=0)
    water_consumption: float = Field(ge=0)
    waste_generated: float = Field(ge=0)
    recycling_rate: float = Field(ge=0, le=100)
    renewable_energy: float = Field(ge=0, le=100)
    transport_emissions: float = Field(ge=0)
    carbon_emissions: float = Field(ge=0)


# COMPANY SCHEMAS

class CompanyCreate(BaseModel):
    company_name: str
    industry: str
    employees: int
    annual_revenue: float
    country: str

# USER REGISTRATION

class UserRegister(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    company: str
    password: str

# USER LOGIN

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# JWT TOKEN

class Token(BaseModel):
    access_token: str
    token_type: str