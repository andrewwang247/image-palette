"""Test image palette clustering.

Copyright 2026. Andrew Wang.
"""

from typing import TYPE_CHECKING

import pandas as pd
import pytest

from .conftest import CLUSTER_RNG

if TYPE_CHECKING:
    from .conftest import Solution


@pytest.mark.parametrize("clusters", CLUSTER_RNG)
def test_cluster(solution: Solution, clusters: int) -> None:
    """Validate clustering produces correct centroids."""
    actual_df = solution.clustering.compute_palette(clusters)
    expected_df = solution.palette[clusters]
    pd.testing.assert_frame_equal(
        actual_df.sort_values(by="hex").reset_index(drop=True),
        expected_df.sort_values(by="hex").reset_index(drop=True),
    )
