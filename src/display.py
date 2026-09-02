"""Display palette in a webpage using a template.

Copyright 2026. Andrew Wang.
"""

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pandas as pd
from jinja2 import Environment, FileSystemLoader, Template

TEMPLATE_DIR = "templates"
TEMPLATE_NAME = "palette.jinja"

logger = logging.getLogger(__name__)


def _get_template() -> Template:
    """Get Jinja template from file system."""
    current_script_dir = Path(__file__).resolve().parent
    root_dir = current_script_dir.parent
    jinja_env = Environment(
        loader=FileSystemLoader(root_dir / TEMPLATE_DIR), autoescape=True
    )
    return jinja_env.get_template(TEMPLATE_NAME)


def _format_dataframe(df: pd.DataFrame) -> list[dict[str, Any]]:
    """Format DataFrame as list of color / percentage objects."""
    colors = []
    for row in df.itertuples(index=False):
        logger.info("Formatting DataFrame row %s", row)
        item = {"color": row.hex, "percentage": row.prevalence}
        colors.append(item)
    return colors


def render_page(fname: str, df: pd.DataFrame) -> str:
    """Display palette in a webpage."""
    logger.info("Loading Jinja template from file system")
    template = _get_template()
    path = Path(fname)
    logger.info("Rendering template with palette data")
    return template.render(
        filename=path.name, filepath=path, palette=_format_dataframe(df)
    )
