from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated


tier_1_cities = ["Mumbai", "Delhi", "Bangalore",
                 "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]


# validate data

class UserData(BaseModel):
    age: Annotated[int, Field(..., ge=0, le=120,
                              description="Age must be between 0 and 120")]
    weight: Annotated[float, Field(..., gt=0,
                                   description="Weight must be greater than 0")]
    height: Annotated[float, Field(..., gt=0,
                                   description="Height must be greater than 0")]
    income_lpa: Annotated[float,
                          Field(..., gt=0, description="Income LPA must be greater than 0")]
    smoker: Annotated[bool,
                      Field(..., description="Smoker must be either true or false")]
    city: Annotated[str, Field(..., description="City must be a string")]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
                                  'business_owner', 'unemployed', 'private_job'],
                          Field(..., description="Occupation must be one of the specified values")]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, value: str) -> str:
        v = value.strip().title()
        return v

# now compute the new features from the user data

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle-aged'
        else:
            return 'senior'

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
