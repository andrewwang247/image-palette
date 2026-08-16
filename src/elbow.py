"""
Find the optimal number of clusters with the elbow method.

Copyright 2026. Andrew Wang.
"""
import logging
import numpy as np
from tqdm import tqdm
from kneed import KneeLocator  # type: ignore
from sklearn.cluster import KMeans  # type: ignore

MIN_CLUSTERS = 3
MAX_CLUSTERS = 8
logger = logging.getLogger(__name__)


def cluster_count(pixels: np.ndarray[tuple[int, int]], verbose: bool) -> int:
    """Use elbow method to find optimal number of clusters."""
    logger.info(
        'Using elbow method to find best clustering between %d and %d',
        MIN_CLUSTERS, MAX_CLUSTERS)

    inertias = []
    cluster_range = range(MIN_CLUSTERS, MAX_CLUSTERS + 1)
    for n_clusters in (cluster_range if verbose else tqdm(cluster_range)):
        kms = KMeans(n_clusters, verbose=1 if verbose else 0)
        kms.fit(pixels)
        inertias.append(kms.inertia_)

    knee_locator = KneeLocator(
        x=range(MIN_CLUSTERS, MAX_CLUSTERS + 1),
        y=inertias,
        curve='convex',
        direction='decreasing'
    )

    elbow = knee_locator.elbow
    assert elbow is not None, 'Did not find an elbow'
    logger.info('Detected elbow at %d clusters', elbow)
    return int(elbow)
