# Recipe Optimizer API

This project provides a FastAPI-based service to optimize a recipe by selecting the cheapest alternative components with the same similarity index, while adhering to user-defined constraints such as melting point and country of production.

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

# Recipe Optimizer API

This project provides a FastAPI-based service to optimize a recipe by selecting the cheapest alternative components with the same similarity index, while adhering to user-defined constraints such as melting point and country of production.

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
`
{
  "components": [
    {"similarity_index": "6489", "amount": 0.1},
    {"similarity_index": "231", "amount": 0.2},
    {"similarity_index": "54", "amount": 0.7}
  ],
  "melting_point": 200,
  "country": "China"
}
`
Response Model
`
{
  "optimized_recipe": [
    {
      "raw_material_id": "V4W8XAKYN59WBM1X",
      "similarity_index": "6489",
      "amount": 0.1,
      "price": 6.1,
      "cost": 0.61
    },
    {
      "raw_material_id": "P5XJ8TYFZZPV79EX",
      "similarity_index": "231",
      "amount": 0.2,
      "price": 15.0,
      "cost": 3.0
    },
    {
      "raw_material_id": "14KRYBWKFWRA891P",
      "similarity_index": "54",
      "amount": 0.7,
      "price": 2.8,
      "cost": 1.96
    }
  ],
  "total_cost": 5.57
}
`
