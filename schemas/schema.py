import os
from typing import List
from pydantic import BaseModel, Field, validator


class Component(BaseModel):
    similarity_index: str
    amount: float = Field(..., gt=0, le=1, description="Amount as a fraction (e.g., 0.1 for 10%)")

    @validator("amount")
    def validate_amount(cls, value):
        if value <= 0 or value > 1:
            raise ValueError("Amount must be between 0 and 1.")
        return value

class RecipeRequest(BaseModel):
    components: List[Component]
    melting_point: float = Field(..., gt=0, description="Minimum melting point in °C")
    country: str = Field(..., description="Country where the recipe is to be produced")

    @validator("components")
    def validate_total_amount(cls, components):
        total_amount = sum(component.amount for component in components)
        if not (0.99 <= total_amount <= 1.01):  # Allowing a small margin for floating-point precision
            raise ValueError("The total amount of all components must sum to 1 (100%).")
        return components