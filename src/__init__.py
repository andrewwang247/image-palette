"""
Pixel clustering with K-Means.

Copyright 2026. Andrew Wang
"""
# pylint: disable=useless-import-alias

from .elbow import cluster_count as cluster_count, \
    MIN_CLUSTERS as MIN_CLUSTERS, MAX_CLUSTERS as MAX_CLUSTERS
from .lab import get_pixels as get_pixels
from .cluster import compute_palette as compute_palette
from .display import render_page as render_page
