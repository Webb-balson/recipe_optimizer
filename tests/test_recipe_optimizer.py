import pandas as pd
import pytest
from src.recipe_price_optimization import RecipeOptimizer

class TestRecipeOptimizer:

    @pytest.fixture
    def setup_optimizer(self):
        file_path = "data/ingredients_info.csv"
        optimizer = RecipeOptimizer(file_path)
        optimizer.load_data()
        return optimizer

    def test_load_data(self, setup_optimizer):
        optimizer = setup_optimizer
        assert optimizer.data is not None
        assert not optimizer.data.empty

    def test_filter_data(self, setup_optimizer):
        optimizer = setup_optimizer
        optimizer.filter_data()
        assert not optimizer.data.empty
        assert all(optimizer.data['Melting Point'] >= 200)
        assert all(optimizer.data['Availability in Country'].str.contains('China'))

    def test_optimize_recipe(self, setup_optimizer):
        optimizer = setup_optimizer
        optimizer.filter_data()
        optimized_recipe = optimizer.optimize_recipe()
        assert len(optimized_recipe) == 3
        assert all(optimized_recipe['Proportion'].isin([0.1, 0.2, 0.7]))
        assert 'Cost' in optimized_recipe.columns

    def test_run(self, setup_optimizer):
        optimized_recipe = setup_optimizer.run()
        assert not optimized_recipe.empty
        assert 'Cost' in optimized_recipe.columns