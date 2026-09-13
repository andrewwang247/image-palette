"""Test image palette clustering.

Copyright 2026. Andrew Wang.
"""

from pathlib import Path

import pandas as pd
import pytest

from src import MAX_ELBOW_CLUSTERS, MIN_ELBOW_CLUSTERS, Clustering, FloatGrid, Pixels


def _get_clusters() -> list[tuple[FloatGrid, pd.DataFrame]]:
    """Load images and cluster solutions."""
    df = pd.read_csv("test/cluster.csv")
    images = df.image.unique()
    tests = []
    for img in images:
        img_path = Path("images") / f"{img}.jpg"
        img_df = df[df.image == img].drop(columns=["image"])
        pixels = Pixels(img_path).as_ok_lab()
        for clusters in range(MIN_ELBOW_CLUSTERS, MAX_ELBOW_CLUSTERS + 1):
            sub_df = img_df[img_df.clusters == clusters].drop(columns=["clusters"])
            tests.append((pixels, sub_df))
    return tests


@pytest.mark.parametrize(("pixels", "expected_df"), _get_clusters())
def test_cluster(
    random_seed: int, pixels: FloatGrid, expected_df: pd.DataFrame
) -> None:
    """Test clustering for images."""
    clustering = Clustering(pixels, random_seed)
    actual_df = clustering.compute_palette(expected_df.shape[0])
    pd.testing.assert_frame_equal(
        actual_df.sort_values(by="hex").reset_index(drop=True),
        expected_df.sort_values(by="hex").reset_index(drop=True),
    )
