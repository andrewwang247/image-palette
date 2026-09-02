"""Extract color palette from provided image.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path

from click import Path as cPath
from click import command, option

from src import cluster_count, compute_palette, get_pixels, render_page


@command()
@option(
    "--filename",
    "-f",
    required=True,
    type=cPath(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="Path to image file.",
)
@option(
    "--clusters",
    "-c",
    required=False,
    type=int,
    default=None,
    help="Number of palette colors. Automatic if not set.",
)
@option(
    "--output",
    "-o",
    required=False,
    type=cPath(exists=False),
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
    filename: str, clusters: int | None, output: str | None, *, verbose: bool
) -> None:
    """Extract color palette from provided image."""
    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    pixels = get_pixels(Path(filename))
    optimal_k = cluster_count(pixels, verbose=verbose) if clusters is None else clusters
    df = compute_palette(pixels, optimal_k, verbose=verbose)
    print(df.to_string(index=False))
    if output is None:
        return
    html = render_page(filename, df)
    with Path(output).open("w", encoding="UTF-8") as fp:
        fp.write(html)


if __name__ == "__main__":
    main()
