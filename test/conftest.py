"""Configure pytest fixtures.

Copyright 2026. Andrew Wang.
"""

import pytest


@pytest.fixture(scope="session")
def random_seed() -> int:
    """Provide fixed random seed."""
    return 42
