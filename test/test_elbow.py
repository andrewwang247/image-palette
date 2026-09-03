"""Test elbow method for selecting number of clusters.

Copyright 2026. Andrew Wang.
"""

from json import load
from pathlib import Path

import pytest

from src import Clustering, Pixels

RANDOM_SEED = 42


def _get_elbows() -> list[tuple[Path, int]]:
    """Load images and elbow solutions."""
    with Path("test/elbow.json").open(encoding="UTF-8") as fp:
        elbows: dict[str, int] = load(fp)
    return [(Path(key), value) for key, value in elbows.items()]


@pytest.mark.parametrize(("image_path", "expected_clusters"), _get_elbows())
def test_elbow(image_path: Path, expected_clusters: int) -> None:
    """Test elbow method for images."""
    pixels = Pixels(image_path)
    clustering = Clustering(pixels.as_ok_lab(), RANDOM_SEED)
    actual_clusters = clustering.cluster_count()
    assert expected_clusters == actual_clusters
