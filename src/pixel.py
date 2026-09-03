"""Convert between sRGB and OkLAB image formats.

Copyright 2026. Andrew Wang.
"""

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

import numpy as np
from colour.models import Oklab_to_XYZ, XYZ_to_Oklab, XYZ_to_sRGB, sRGB_to_XYZ
from PIL import Image

SRGB_SCALING = 255.0
logger = logging.getLogger(__name__)

MAX_DIM = (1024, 1024)

type IntGrid = np.ndarray[tuple[int, int], np.dtype[np.int_]]
type FloatGrid = np.ndarray[tuple[int, int], np.dtype[np.floating[Any]]]


class Pixels:
    """Image conversion between sRGB and OkLAB."""

    def __init__(self, fpath: Path) -> None:
        """Import image file from path and downsize."""
        logger.info("Opening image file %s", fpath)
        self.img = Image.open(fpath)
        logger.info("Before resampling: %d x %d px", self.img.width, self.img.height)
        self.img.thumbnail(MAX_DIM, Image.Resampling.LANCZOS)
        logger.info("After resampling: %d x %d px", self.img.width, self.img.height)

    def as_ok_lab(self) -> FloatGrid:
        """Convert Image to OkLAB format."""
        img_arr = np.array(self.img.convert("RGB")) / SRGB_SCALING
        logger.info("Converting from sRGB to CIE XYZ")
        img_xyz = sRGB_to_XYZ(img_arr)
        logger.info("Converting from CIE XYZ to Oklab")
        img_lab = XYZ_to_Oklab(img_xyz)
        return img_lab.reshape(-1, 3)

    @staticmethod
    def to_rgb(lab_arr: FloatGrid) -> IntGrid:
        """Convert OK lab pixels into denormalized sRGB."""
        logger.info("Converting from Oklab to CIE XYZ")
        xyz_arr = Oklab_to_XYZ(lab_arr)
        logger.info("Converting from CIE XYZ to sRGB")
        rgb_arr = XYZ_to_sRGB(xyz_arr)
        return np.round(SRGB_SCALING * rgb_arr).astype(np.int_)
