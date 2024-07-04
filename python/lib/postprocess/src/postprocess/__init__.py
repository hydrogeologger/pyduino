"""This package contains modules and functions to assist with post processing.

Dependencies:
- matplotlib
- numpy
- pandas
"""

# Module Info
__version__ = "0.1.0"

from .interpolation import Interpolation
from .pandas_utils import (
    flatten_column_headers,
    insert_index_level,
    swap_index,
    unique_index_levels_only,
)
from .transformation import (
    calculate_delta,
    normalise,
)
