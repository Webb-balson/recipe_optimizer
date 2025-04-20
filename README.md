# Recipe Optimizer API

This project provides a FastAPI-based service to optimize a recipe by selecting the cheapest alternative components with the same similarity index, while adhering to user-defined constraints such as melting point and country of production.

---

## Approach and Assumptions

### Approach

From the assessment, I understood that to create a recipe, multiple components are required, and their total amount must sum to 100%. There are restrictions for creating a recipe, such as:

1. The component must have a defined melting point.
2. The component must be available in the specified country.

The goal is to optimize the recipe to minimize the total cost while adhering to these restrictions. From the dataset, I observed that for a given component, there are multiple alternatives with the same similarity index. The price of these alternatives varies based on their melting point and country availability.

My approach was to identify alternate components with the same similarity index that satisfy the given restrictions and select the one with the minimum cost for the recipe.

### Assumptions

1. A component with the same similarity index can be substituted with an alternative from another country if the original component is unavailable due to the provided restrictions.
2. To simplify the process, I performed data transformations on the provided CSV file:
  - Converted prices from string format (e.g., `$6.50`) to numeric format (e.g., `6.5`).
  - Handled country availability using categorized lists such as `all`, `exclude`, and `include`.

This approach ensures that the recipe is optimized for cost while adhering to the constraints.

---

## Features

- Load ingredient data from a CSV file.
- Filter ingredients based on melting point and country availability.
- Optimize the recipe by selecting the cheapest components with the same similarity index.
- Validate user input to ensure the total amount of components sums to 100%.
- Return the optimized recipe with the total cost.

---

## Requirements

- Python 3.11 or higher
- FastAPI
- Uvicorn

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/recipe_optimizer.git
   cd recipe_optimizer

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt

4. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload

## API Endpoint

### POST /optimize-recipe

Optimize a recipe by selecting the cheapest components with the same similarity index, based on user-defined constraints.

Request Model
  ```json
  {
    "components": [
      {"raw_material_id": "6Z9K9FXGBN9Y1GXA", "similarity_index": "6489", "amount": 0.1},
      {"raw_material_id": "6Z9K9FXGBN9Y1GXA", "similarity_index": "231", "amount": 0.2},
      {"raw_material_id": "6Z9K9FXGBN9Y1GXA", "similarity_index": "54", "amount": 0.7}
    ],
    "melting_point": 200,
    "country": "China"
  }

Response Model
  ```json
  {
    "optimized_recipe": [
      {
        "raw_material_id": "9Z70ZMMBEA1863YG",
        "similarity_index": "6489",
        "amount": 0.1,
        "price": "$6.50",
        "cost": "$0.65"
      },
      {
        "raw_material_id": "P5XJ8TYFZZPV79EX",
        "similarity_index": "231",
        "amount": 0.2,
        "price": "$15.00",
        "cost": "$3.00"
      },
      {
        "raw_material_id": "14KRYBWKFWRA891P",
        "similarity_index": "54",
        "amount": 0.7,
        "price": "$2.80",
        "cost": "$1.96"
      }
    ],
    "total_cost": "$5.61"
  }

