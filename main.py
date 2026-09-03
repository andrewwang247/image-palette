"""Extract color palette from provided image.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path
from typing import TextIO

from click import File, IntRange, command, option
from click import Path as cPath

from src import Clustering, Display, Pixels


@command()
@option(
    "--image_path",
    "-i",
    required=True,
    type=cPath(
        exists=True, file_okay=True, dir_okay=False, readable=True, path_type=Path
    ),
    help="Path to image file.",
)
@option(
    "--clusters",
    "-c",
    required=False,
    type=IntRange(1, 10),
    default=None,
    help="Number of palette colors. Automatic if not set.",
)
@option(
    "--output_file",
    "-o",
    required=False,
    type=File("w", encoding="UTF-8"),
    help="Path to output html.",
)
@option(
    "--verbose",
    "-v",
    is_flag=True,
    default=False,
    help="Displays application logs if set.",
)
def main(
    image_path: Path, clusters: int | None, output_file: TextIO | None, *, verbose: bool
) -> None:
    """Extract color palette from provided image."""
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    pixels = Pixels(image_path)
    clustering = Clustering(pixels.as_ok_lab(), verbose=verbose)
    num_colors = clusters or clustering.cluster_count()
    df = clustering.compute_palette(num_colors)
    print(df.to_string(index=False))
    if output_file:
        display = Display()
        html = display.render_page(image_path, df)
        output_file.write(html)


if __name__ == "__main__":
    main()
