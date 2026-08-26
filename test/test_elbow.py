"""
Test elbow method for selecting number of clusters.

Copyright 2026. Andrew Wang.
"""
from typing import Dict, List, Tuple
from json import load
from pytest import mark
from src import get_pixels, cluster_count

RANDOM_SEED = 42


def _get_elbows() -> List[Tuple[str, int]]:
    """Load images and elbow solutions."""
    with open('test/elbow.json', encoding='UTF-8') as fp:
        elbows: Dict[str, int] = load(fp)
    return list(elbows.items())


@mark.parametrize('image_path,expected_clusters', _get_elbows())
def test_elbow(image_path: str, expected_clusters: int) -> None:
    """Test elbow method for images."""
    pixels = get_pixels(image_path)
    actual_clusters = cluster_count(pixels, rand_state=RANDOM_SEED)
    assert expected_clusters == actual_clusters
