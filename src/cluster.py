"""Compute pixel clustering of image colors.

Copyright 2026. Andrew Wang.
"""

import logging

import numpy as np
import pandas as pd
from kneed import KneeLocator
from sklearn.cluster import KMeans
from tqdm import tqdm

from .pixel import FloatGrid, Pixels

CLUSTER_INITS = 3
MIN_ELBOW_CLUSTERS = 3
MAX_ELBOW_CLUSTERS = 8

logger = logging.getLogger(__name__)


class Clustering:
    """Cluster image pixels by color to generate palette."""

    def __init__(
        self, pixels: FloatGrid, rand_state: int | None = None, *, verbose: bool = False
    ) -> None:
        """Constructor stores common parameters."""
        self.pixels = pixels
        self.rand_state = rand_state
        self.verbose = verbose

    def compute_palette(self, num_colors: int) -> pd.DataFrame:
        """Compute color palette from image and organize in DataFrame."""
        logger.info("Clustering image pixels into %d palette colors", num_colors)
        kms = self.__get_kms(num_colors, CLUSTER_INITS)
        labels = kms.fit_predict(self.pixels)
        cluster_sizes = np.bincount(labels)
        centers = Pixels.to_rgb(kms.cluster_centers_)
        prevalence = cluster_sizes / np.shape(labels)[0]

        logger.info("Organizing information into DataFrame")
        df = pd.DataFrame(columns=["hex", "red", "green", "blue", "prevalence"])
        df[["red", "green", "blue"]] = centers
        df["prevalence"] = np.round(100 * prevalence, 1)
        df["hex"] = (
            "#"
            + df["red"].map("{:02x}".format)
            + df["green"].map("{:02x}".format)
            + df["blue"].map("{:02x}".format)
        )
        return df.sort_values(by="prevalence", ascending=False)

    def cluster_count(self) -> int:
        """Use elbow method to find optimal number of clusters."""
        logger.info(
            "Using elbow method to find best clustering between %d and %d",
            MIN_ELBOW_CLUSTERS,
            MAX_ELBOW_CLUSTERS,
        )

        cluster_rng = range(MIN_ELBOW_CLUSTERS, MAX_ELBOW_CLUSTERS + 1)
        iter_rng = cluster_rng if self.verbose else tqdm(cluster_rng)
        inertias = [self.__get_kms(n).fit(self.pixels).inertia_ for n in iter_rng]

        knee_locator = KneeLocator(
            x=cluster_rng,
            y=inertias,
            curve="convex",
            direction="decreasing",
        )

        elbow = knee_locator.elbow
        assert elbow is not None, "Did not find an elbow"
        logger.info("Detected elbow at %d clusters", elbow)
        return int(elbow)

    def __get_kms(self, n_clusters: int, n_init: int | None = None) -> KMeans:
        """Initialize a configured KMeans instance with given clusters."""
        return KMeans(
            n_clusters=n_clusters,
            n_init=n_init or "auto",
            random_state=self.rand_state,
            verbose=1 if self.verbose else 0,
        )
