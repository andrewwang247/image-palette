"""Display palette in a webpage using a template.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, FileSystemLoader

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pandas as pd

logger = logging.getLogger(__name__)

_TEMPLATE_DIR = Path("templates")


class Display:
    """Render palette webpages using a template."""

    def __init__(self) -> None:
        """Load Jinja template and store output path."""
        logger.info("Loading Jinja environment from %s directory", _TEMPLATE_DIR)
        jinja_env = Environment(loader=FileSystemLoader(_TEMPLATE_DIR), autoescape=True)

        template_path = _TEMPLATE_DIR / "palette.jinja"
        assert template_path.is_file(), f"No template at {template_path}"
        logger.info("Retrieving Jinja template at %s", template_path)
        self.template = jinja_env.get_template(template_path.name)

    def render_page(self, img_path: Path, df: pd.DataFrame) -> str:
        """Display palette in a webpage."""
        assert img_path.is_file(), f"Path {img_path} is not a file."
        logger.info("Rendering template with palette data for %s", img_path)
        return self.template.render(
            filename=img_path.name,
            filepath=img_path,
            palette=Display.fmt_df(df),
        )

    @staticmethod
    def fmt_df(df: pd.DataFrame) -> Iterable[dict[str, Any]]:
        """Format DataFrame color / percentage objects."""
        for row in df.itertuples(index=False):
            logger.info("Formatting DataFrame row %s", row)
            yield {"color": row.hex, "percentage": row.prevalence}
