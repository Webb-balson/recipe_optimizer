import csv

def load_data(file_path):
    """
    Load the ingredient data from the CSV file.

    :param file_path: Path to the CSV file containing ingredient data.
    :return: A list of dictionaries representing the ingredient data.
    """
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        data = []
        for row in reader:
            row['Price'] = float(row['Price'].replace('$', '').strip())
            row['Melting Point'] = float(row['Melting Point'])
            data.append(row)
    return data

def parse_availability(availability_text):
    """
    Parse the 'Availability in Country' column into a structured format.

    :param availability_text: The raw text from the 'Availability in Country' column.
    :return: A dictionary with 'type' (either 'exclude' or 'include') and 'countries' (list of countries).
    """
    if availability_text.strip() == "ALL":
        return {"type": "exclude", "countries": []}  # No exclusions, available everywhere
    elif availability_text.startswith("ALL except"):
        excluded_countries = [country.strip() for country in availability_text.replace("ALL except", "").split(",")]
        return {"type": "exclude", "countries": excluded_countries}
    elif availability_text.startswith("Only"):
        included_countries = [country.strip() for country in availability_text.replace("Only", "").split(",")]
        return {"type": "include", "countries": included_countries}
    else:
        raise ValueError(f"Unexpected availability format: {availability_text}")

def is_available_in_china(availability):
    """
    Check if a material is available in China based on its parsed availability.

    :param availability: Parsed availability dictionary from `parse_availability`.
    :return: True if the material is available in China, False otherwise.
    """
    if availability["type"] == "exclude":
        return "China" not in availability["countries"]
    elif availability["type"] == "include":
        return "China" in availability["countries"]
    else:
        raise ValueError(f"Unexpected availability type: {availability['type']}")

# Example usage
# availability_texts = [
#     "ALL",
#     "ALL except China",
#     "ALL except Thailand, Indonesia, Germany",
#     "Only Malaysia, Singapore"
# ]

# for text in availability_texts:
#     parsed = parse_availability(text)
#     print(f"Raw: {text}")
#     print(f"Parsed: {parsed}")
#     print(f"Available in China: {is_available_in_china(parsed)}")
#     print()

def filter_data(data):
    """
    Filter the data based on the constraints:
    1. Melting point >= 200°C.
    2. Availability in China.

    :param data: List of ingredient dictionaries.
    :return: Filtered list of ingredient dictionaries.
    """
    filtered_data = []
    for row in data:
        availability = parse_availability(row['Availability in Country'])
        if row['Melting Point'] >= 200 and is_available_in_china(availability):
            filtered_data.append(row)
    return filtered_data

def find_alternative_components(data, target_components):
    """
    Find the cheapest alternative components for the given target components based on similarity index.

    :param data: Filtered list of ingredient dictionaries.
    :param target_components: List of target components with their amounts.
    :return: A list of dictionaries representing the selected components with amounts and costs.
    """
    recipe = []
    for target in target_components:
        similarity_index = target['Similarity Index']
        # Find all components with the same similarity index
        alternatives = [row for row in data if row['Similarity Index'] == similarity_index]
        # Select the cheapest component or pick the target itself if no alternatives are found
        if len(alternatives) != 0:
            cheapest = min(alternatives, key=lambda x: x['Price'])
        else:
            cheapest = {row for row in data if row['Similarity Index'] == similarity_index}
        # Assign the amount and calculate the cost
        cheapest['Amount'] = target['Amount']
        cheapest['Cost'] = cheapest['Price'] * cheapest['Amount']
        recipe.append(cheapest)
    return recipe

def calculate_total_cost(recipe):
    """
    Calculate the total cost of the recipe.

    :param recipe: List of dictionaries representing the recipe.
    :return: Total cost of the recipe.
    """
    return sum(ingredient['Cost'] for ingredient in recipe)

def run(file_path):
    """
    Run the entire optimization process.

    :param file_path: Path to the CSV file containing ingredient data.
    :return: Optimized recipe as a list of dictionaries and the total cost.
    """
    # Load and filter the data
    data = load_data(file_path)
    filtered_data = filter_data(data)

    # Define the target components with their similarity indices and amounts
    target_components = [
        {'Similarity Index': '6489', 'Amount': 0.1},  # 10%
        {'Similarity Index': '231', 'Amount': 0.2},   # 20%
        {'Similarity Index': '54', 'Amount': 0.7}    # 70%
    ]

    # Find the cheapest alternative components
    recipe = find_alternative_components(filtered_data, target_components)

    # Calculate the total cost
    total_cost = calculate_total_cost(recipe)
    return recipe, total_cost

if __name__ == "__main__":
    # Path to the CSV file
    file_path = "/home/webb/recipe_optimizer/recipe_optimizer_project/data/ingredients_info.csv"

    # Run the optimization process
    recipe, total_cost = run(file_path)

    # Print the optimized recipe
    print("Optimized Recipe:")
    for ingredient in recipe:
        print(f"Raw Material ID: {ingredient['Raw Material ID']}, "
              f"Similarity Index: {ingredient['Similarity Index']}, "
              f"Amount: {ingredient['Amount']*100:.0f}%, "
              f"Price: ${ingredient['Price']:.2f}, "
              f"Cost: ${ingredient['Cost']:.2f}")
    print(f"Total Cost: ${total_cost:.2f}")