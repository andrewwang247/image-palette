"""
Extract color palette from provided image.

Copyright 2026. Andrew Wang.
"""
import logging
from click import command, option, Path
from src import cluster_count, get_pixels, compute_palette
# pylint: disable=no-value-for-parameter


@command()
@option('--filename', '-f', required=True,
        type=Path(exists=True, file_okay=True, dir_okay=False, readable=True),
        help='Path to image file.')
@option('--clusters', '-c', required=False, type=int, default=None,
        help='Number of palette colors. Automatic if not set.')
@option('--verbose', '-v', is_flag=True, default=False,
        help='Displays application logs if set.')
def main(filename: str, clusters: int | None, verbose: bool) -> None:
    """Handle user input and run palette extraction."""
    logging.basicConfig(level=logging.INFO if verbose else logging.WARN)
    pixels = get_pixels(filename)
    optimal_k = cluster_count(
        pixels, verbose) if clusters is None else clusters
    df = compute_palette(pixels, optimal_k, verbose)
    print(df.to_string(index=False))


if __name__ == '__main__':
    main()
