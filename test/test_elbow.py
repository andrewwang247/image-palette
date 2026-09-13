"""Test elbow method for selecting number of clusters.

Copyright 2026. Andrew Wang.
"""

from json import load
from pathlib import Path

import pytest

from src import Clustering, FloatGrid, Pixels


def _get_elbows() -> list[tuple[FloatGrid, int]]:
    """Load images and elbow solutions."""
    with Path("test/elbow.json").open(encoding="UTF-8") as fp:
        elbows: dict[str, int] = load(fp)
    params: list[tuple[FloatGrid, int]] = []
    for fname, expected_elbow in elbows.items():
        pixels = Pixels(Path(fname))
        params.append((pixels.as_ok_lab(), expected_elbow))
    return params


@pytest.mark.parametrize(("pixels", "expected_clusters"), _get_elbows())
def test_elbow(random_seed: int, pixels: FloatGrid, expected_clusters: int) -> None:
    """Test elbow method for images."""
    clustering = Clustering(pixels, random_seed)
    actual_clusters = clustering.cluster_count()
    assert actual_clusters == expected_clusters
