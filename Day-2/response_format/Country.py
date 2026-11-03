from pydantic import BaseModel, Field
# {'country_id': 'SG', 'probability': 0.009201}

class Country(BaseModel):
    country_id: str = Field(description="The country code representing the country associated with the given name.")
    probability: float = Field(description="The probability of the given name being associated with the specified country.")
    
class NamePredictionResult(BaseModel):
    name: str = Field(description="The name for which nationality information is being predicted.")
    country: list[Country] = Field(description="A list of countries with their associated probabilities for the given name.")
    top_country: Country = Field(description="The country with the highest probability for the given name.")


class NamePredictionResults(BaseModel):
    predictions: list[NamePredictionResult] = Field(
        description="One nationality prediction result for each requested name."
    )