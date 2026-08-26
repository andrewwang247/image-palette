# Image Palette

Extract perceptually accurate color palettes representative of the dominant hues in an image. User can either specify the number of colors in the palette or let the software choose algorithmically. A table of colors and their prevalence is logged to stdout. If the `output` option is specified, a webpage is generated that previews the image alongside the palette colors.

## Usage

```text
Usage: main.py [OPTIONS]

  Extract color palette from provided image.

Options:
  -f, --filename FILE     Path to image file.  [required]
  -c, --clusters INTEGER  Number of palette colors. Automatic if not set.
  -o, --output PATH       Path to output html.
  -v, --verbose           Displays application logs if set.
  --help                  Show this message and exit.
```

## Methodology

1. The input image is downscaled to a maximum dimensionality of $1024 \times 1024$ with [LANCZOS resampling](https://en.wikipedia.org/wiki/Lanczos_resampling). Aspect ratio and relative color frequency is preserved. This pre-processing step dramatically speeds up computation for large images.
2. Typically, raster images use RGB to represent pixel values. We transform to the [Oklab color space](https://en.wikipedia.org/wiki/Oklab_color_space) for improved perceptual uniformity when generating the palette. The output is converted back into RGB for compatibility.
3. We use [K-means clustering](https://en.wikipedia.org/wiki/K-means_clustering) on the Oklab pixel values. The cluster means correspond to the image's representative palette colors. The relative frequency of labels assigned to each mean correspond to the color's prevalence.
4. If the number of colors / clusters is not specified, we use the [elbow method](https://en.wikipedia.org/wiki/Elbow_method_\(clustering\)) to find the optimal quantity between 3 and 8, inclusive.
5. If an output file is specified, we generate a webpage from a Jinja template. The webpage displays the image and a preview of the palette colors alongside their hex codes and prevalence.

## Acknowledgements

This project was inspired by [Lokesh Dhakar's](https://lokeshdhakar.com/) and his [Color Thief](https://lokeshdhakar.com/projects/color-thief/) npm package. Our version uses K-means clustering rather than [median cut](https://en.wikipedia.org/wiki/Median_cut). All photos in the `images` directory are &copy; 2026 Andrew Wang. Licensed under [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
