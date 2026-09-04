"""Test elbow method for selecting number of clusters.

Copyright 2026. Andrew Wang.
"""

from json import load
from pathlib import Path

import pytest

from src import Clustering, Pixels

RANDOM_SEED = 42


def _get_elbows() -> list[tuple[Pixels, int]]:
    """Load images and elbow solutions."""
    with Path("test/elbow.json").open(encoding="UTF-8") as fp:
        elbows: dict[str, int] = load(fp)
    return [(Pixels(Path(key)), value) for key, value in elbows.items()]


@pytest.mark.parametrize(("pixels", "expected_clusters"), _get_elbows())
def test_elbow(pixels: Pixels, expected_clusters: int) -> None:
    """Test elbow method for images."""
    clustering = Clustering(pixels.as_ok_lab(), RANDOM_SEED)
    actual_clusters = clustering.cluster_count()
    assert expected_clusters == actual_clusters
