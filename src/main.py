from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import List
from pathlib import Path

from reciepe_optimizer_project.schemas.schema import RecipeRequest
from utils.util import DataLoader, AvailabilityParser, RecipeOptimizer

app = FastAPI()


@app.post("/optimize-recipe")
def optimize_recipe(request: RecipeRequest):
    # Path to the CSV file
    file_path = "/home/webb/recipe_optimizer/recipe_optimizer_project/data/ingredients_info.csv"

    # Load data using DataLoader
    try:
        data = DataLoader.load_data(file_path)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Initialize RecipeOptimizer with the loaded data
    optimizer = RecipeOptimizer(data)

    # Filter data based on melting point and country
    try:
        filtered_data = optimizer.filter_data(request.melting_point, request.country)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Find alternative components for the recipe
    try:
        recipe = optimizer.find_alternative_components(request.components)
    except HTTPException as e:
        raise e

    # Calculate the total cost of the recipe
    total_cost = RecipeOptimizer.calculate_total_cost(recipe)

    # Return the optimized recipe and total cost
    return {
        "optimized_recipe": [
            {
                "raw_material_id": ingredient['Raw Material ID'],
                "similarity_index": ingredient['Similarity Index'],
                "amount": ingredient['Amount'],
                "price": ingredient['Price'],
                "cost": ingredient['Cost']
            }
            for ingredient in recipe
        ],
        "total_cost": total_cost
    }