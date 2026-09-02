"""Convert between sRGB and OkLAB image formats.

Copyright 2026. Andrew Wang.
"""

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import numpy as np
import numpy.typing as npt
from colour.models import Oklab_to_XYZ, XYZ_to_Oklab, XYZ_to_sRGB, sRGB_to_XYZ
from PIL import Image

SRGB_SCALING = 255.0
logger = logging.getLogger(__name__)

MAX_DIM = (1024, 1024)


def _to_lab(img: Image.Image) -> npt.NDArray[np.floating[Any]]:
    """Convert Image to Oklab format."""
    img_arr = np.array(img.convert("RGB")) / SRGB_SCALING
    logger.info("Converting from sRGB to CIE XYZ")
    img_xyz = sRGB_to_XYZ(img_arr)
    logger.info("Converting from CIE XYZ to Oklab")
    img_lab = XYZ_to_Oklab(img_xyz)
    return img_lab.reshape(-1, 3)


def get_pixels(fpath: Path) -> npt.NDArray[np.floating[Any]]:
    """Convert image file into flat pixel array in Ok LAB space."""
    logger.info("Opening image file %s", fpath)
    img = Image.open(fpath)
    logger.info("Before resampling: %d x %d px", img.width, img.height)
    img.thumbnail(MAX_DIM, Image.Resampling.LANCZOS)
    logger.info("After resampling: %d x %d px", img.width, img.height)
    return _to_lab(img)


def to_rgb(lab_arr: npt.NDArray[np.float64]) -> npt.NDArray[np.int_]:
    """Convert OK lab pixels into denormalized sRGB."""
    logger.info("Converting from Oklab to CIE XYZ")
    xyz_arr = Oklab_to_XYZ(lab_arr)
    logger.info("Converting from CIE XYZ to sRGB")
    rgb_arr = XYZ_to_sRGB(xyz_arr)
    return np.round(SRGB_SCALING * rgb_arr).astype(np.int_)
