from pydantic import BaseModel, Field

from typing import Dict


class Response(BaseModel):
    predicted_category: str = Field(
        ..., description="The predicted category for the input data", example="High")
    confidence: float = Field(
        ..., description="The confidence score(0-1) of the prediction", example=0.85)
    class_probabilities: Dict[str, float] = Field(..., description="A dictionary mapping class labels to their corresponding probabilities", example={
                                                  "Low": 0.1, "Medium": 0.05, "High": 0.85})
