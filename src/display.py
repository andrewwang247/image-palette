"""Display palette in a webpage using a template.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    import pandas as pd
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "templates"
TEMPLATE_NAME = "palette.jinja"

logger = logging.getLogger(__name__)


class Display:
    """Render palette webpages using a template."""

    def __init__(self) -> None:
        """Load Jinja template and store output path."""
        current_script_dir = Path(__file__).resolve().parent
        root_dir = current_script_dir.parent
        logger.info("Loading Jinja template from file system")
        jinja_env = Environment(
            loader=FileSystemLoader(root_dir / TEMPLATE_DIR), autoescape=True
        )
        self.template = jinja_env.get_template(TEMPLATE_NAME)

    def render_page(self, img_path: Path, df: pd.DataFrame) -> str:
        """Display palette in a webpage."""
        logger.info("Rendering template with palette data")
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
