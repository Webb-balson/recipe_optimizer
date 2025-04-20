import csv
from fastapi import HTTPException
from typing import List, Dict
from pydantic import BaseModel
from pathlib import Path


class DataLoader:
    """
    A utility class to load data from a CSV file.
    """

    @staticmethod
    def load_data(file_path: str) -> List[Dict]:
        """
        Load data from a CSV file and parse it into a list of dictionaries.

        Args:
            file_path (str): Path to the CSV file.

        Returns:
            List[Dict]: A list of dictionaries containing the parsed data.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If there is an issue parsing the data.
        """
        try:
            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                data = []
                for row in reader:
                    # Convert 'Price' and 'Melting Point' to appropriate data types
                    row['Price'] = float(row['Price'].replace('$', '').strip())
                    row['Melting Point'] = float(row['Melting Point'])
                    data.append(row)
            return data
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except ValueError as e:
            raise ValueError(f"Error parsing data from file {file_path}: {e}")


class AvailabilityParser:
    """
    A utility class to parse and evaluate availability information.
    """

    @staticmethod
    def parse_availability(availability_text: str) -> Dict:
        """
        Parse availability information from a text string.

        Args:
            availability_text (str): The availability text to parse.

        Returns:
            Dict: A dictionary representing the availability.

        Raises:
            ValueError: If the availability format is unexpected.
        """
        if availability_text.strip() == "ALL":
            return {"type": "exclude", "countries": []}
        elif availability_text.startswith("ALL except"):
            excluded_countries = [country.strip() for country in availability_text.replace("ALL except", "").split(",")]
            return {"type": "exclude", "countries": excluded_countries}
        elif availability_text.startswith("Only"):
            included_countries = [country.strip() for country in availability_text.replace("Only", "").split(",")]
            return {"type": "include", "countries": included_countries}
        else:
            raise ValueError(f"Unexpected availability format: {availability_text}")

    @staticmethod
    def is_available_in_country(availability: Dict, country: str) -> bool:
        """
        Check if a product is available in a specific country.

        Args:
            availability (Dict): The availability dictionary.
            country (str): The country to check.

        Returns:
            bool: True if available, False otherwise.

        Raises:
            ValueError: If the availability type is unexpected.
        """
        if availability["type"] == "exclude":
            return country not in availability["countries"]
        elif availability["type"] == "include":
            return country in availability["countries"]
        else:
            raise ValueError(f"Unexpected availability type: {availability['type']}")


class RecipeOptimizer:
    """
    A class to optimize recipes based on data and constraints.
    """

    def __init__(self, data: List[Dict]):
        """
        Initialize the RecipeOptimizer with data.

        Args:
            data (List[Dict]): The data to use for optimization.
        """
        self.data = data

    def filter_data(self, melting_point: float, country: str) -> List[Dict]:
        """
        Filter data based on melting point and country availability.

        Args:
            melting_point (float): The minimum melting point.
            country (str): The country to check availability for.

        Returns:
            List[Dict]: A list of filtered data.
        """
        filtered_data = []
        for row in self.data:
            try:
                # Parse availability and check conditions
                availability = AvailabilityParser.parse_availability(row['Availability in Country'])
                if row['Melting Point'] >= melting_point and AvailabilityParser.is_available_in_country(availability, country):
                    filtered_data.append(row)
            except ValueError as e:
                # Log or handle unexpected availability format
                raise ValueError(f"Error processing row {row}: {e}")
        return filtered_data

    def find_alternative_components(self, target_components: List[BaseModel]) -> List[Dict]:
        """
        Find alternative components for a recipe based on similarity index.

        Args:
            target_components (List[BaseModel]): The target components to find alternatives for.

        Returns:
            List[Dict]: A list of alternative components.

        Raises:
            HTTPException: If no alternatives are found for a similarity index.
        """
        recipe = []
        for target in target_components:
            similarity_index = target.similarity_index
            # Find alternatives with the same similarity index
            alternatives = [row for row in self.data if row['Similarity Index'] == similarity_index]
            if not alternatives:
                raise HTTPException(status_code=404, detail=f"No alternatives found for similarity index {similarity_index}")
            # Select the cheapest alternative
            cheapest = min(alternatives, key=lambda x: x['Price'])
            cheapest['Amount'] = target.amount
            cheapest['Cost'] = cheapest['Price'] * cheapest['Amount']
            recipe.append(cheapest)
        return recipe

    @staticmethod
    def calculate_total_cost(recipe: List[Dict]) -> float:
        """
        Calculate the total cost of a recipe.

        Args:
            recipe (List[Dict]): The recipe to calculate the cost for.

        Returns:
            float: The total cost of the recipe.
        """
        return sum(ingredient['Cost'] for ingredient in recipe)
