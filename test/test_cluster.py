"""Test image palette clustering.

Copyright 2026. Andrew Wang.
"""

from pathlib import Path

import pandas as pd
import pytest

from src import MAX_CLUSTERS, MIN_CLUSTERS, compute_palette, get_pixels

RANDOM_SEED = 42


def _get_clusters() -> list[tuple[Path, pd.DataFrame]]:
    """Load images and cluster solutions."""
    df = pd.read_csv("test/cluster.csv")
    images = df.image.unique()
    tests = []
    for img in images:
        img_path = Path("images") / f"{img}.jpg"
        for clusters in range(MIN_CLUSTERS, MAX_CLUSTERS + 1):
            sub_df = df[(df.image == img) & (df.clusters == clusters)]
            sub_df = sub_df.drop(columns=["image", "clusters"])
            tests.append((img_path, sub_df))
    return tests


@pytest.mark.parametrize(("image_path", "expected_df"), _get_clusters())
def test_cluster(image_path: Path, expected_df: pd.DataFrame) -> None:
    """Test clustering for images."""
    pixels = get_pixels(image_path)
    actual_df = compute_palette(pixels, expected_df.shape[0], rand_state=RANDOM_SEED)
    pd.testing.assert_frame_equal(
        expected_df.sort_values(by="hex").reset_index(drop=True),
        actual_df.sort_values(by="hex").reset_index(drop=True),
    )
