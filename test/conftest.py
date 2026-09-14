"""Configure pytest fixtures.

Copyright 2026. Andrew Wang.
"""

from dataclasses import dataclass
from json import load
from pathlib import Path

import pandas as pd
import pytest

from src import MAX_ELBOW_CLUSTERS, MIN_ELBOW_CLUSTERS, Clustering, Pixels

CLUSTER_RNG = range(MIN_ELBOW_CLUSTERS, MAX_ELBOW_CLUSTERS + 1)
_IMAGES = [img for img in Path("images").iterdir() if img.is_file()]
_RESOURCE_DIR = Path("resources")
_RANDOM_SEED = 42


@dataclass
class Solution:
    """Solution for a single image with expected values."""

    clustering: Clustering
    elbow: int
    palette: dict[int, pd.DataFrame]


@pytest.fixture(scope="session", params=_IMAGES)
def solution(request: pytest.FixtureRequest) -> Solution:
    """Provide solution for a given image."""
    img_path: Path = request.param
    img_name = img_path.stem
    pixels = Pixels(img_path).as_ok_lab()
    clustering = Clustering(pixels, _RANDOM_SEED)

    elbows_path = _RESOURCE_DIR / "elbow.json"
    with elbows_path.open(encoding="UTF-8") as fp:
        elbows: dict[str, int] = load(fp)
    elbow = elbows[img_name]
    assert elbow > 0

    palette: dict[int, pd.DataFrame] = {}
    for n_clusters in CLUSTER_RNG:
        csv_path = _RESOURCE_DIR / f"{img_name}_{n_clusters}.csv"
        df = pd.read_csv(csv_path)
        palette[n_clusters] = df

    return Solution(clustering, elbow, palette)
