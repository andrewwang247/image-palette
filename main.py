"""Extract color palette from provided image.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path
from typing import TextIO

from click import File, IntRange, command, option
from click import Path as cPath

from src import cluster_count, compute_palette, get_pixels, render_page


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
    pixels = get_pixels(image_path)
    optimal_k = cluster_count(pixels, verbose=verbose) if clusters is None else clusters
    df = compute_palette(pixels, optimal_k, verbose=verbose)
    print(df.to_string(index=False))
    if output_file:
        html = render_page(image_path, df)
        output_file.write(html)


if __name__ == "__main__":
    main()
