"""Compute pixel clustering of image colors.

Copyright 2026. Andrew Wang.
"""

import logging
from typing import TYPE_CHECKING, Any

import numpy as np

if TYPE_CHECKING:
    import numpy.typing as npt
import pandas as pd
from sklearn.cluster import KMeans

from .lab import to_rgb

CLUSTER_INITS = 3
logger = logging.getLogger(__name__)


def compute_palette(
    pixels: npt.NDArray[np.floating[Any]],
    num_colors: int,
    rand_state: int | None = None,
    *,
    verbose: bool = False,
) -> pd.DataFrame:
    """Compute color palette from image and organize in DataFrame."""
    logger.info("Clustering image pixels into %d palette colors", num_colors)
    kms = KMeans(
        n_clusters=num_colors,
        n_init=CLUSTER_INITS,
        random_state=rand_state,
        verbose=1 if verbose else 0,
    )
    labels = kms.fit_predict(pixels)
    cluster_sizes = np.bincount(labels)
    centers = to_rgb(kms.cluster_centers_)
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
