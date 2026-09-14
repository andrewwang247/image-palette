"""Test elbow computation.

Copyright 2026. Andrew Wang.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conftest import Solution


def test_elbow(solution: Solution) -> None:
    """Validate that elbow method produces correct value."""
    actual_clusters = solution.clustering.cluster_count()
    assert actual_clusters == solution.elbow
