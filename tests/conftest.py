"""Shared pytest fixtures."""

import pytest

from career_growth.data_generation.generator import generate_all_data


@pytest.fixture(scope="session")
def synthetic_data():
    """Generate a shared synthetic dataset once per test session."""
    return generate_all_data(count=1500, seed=42, output_dir="data_test_shared")
