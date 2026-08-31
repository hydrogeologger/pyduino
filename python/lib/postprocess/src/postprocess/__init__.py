"""This package contains modules and functions to assist with post processing.

Dependencies:
- matplotlib
- numpy
- pandas
"""

# Module Info
__version__ = "0.1.0"

from . import log
from .conversion import (  # Temperature Utilities; Rate Utilities
    celsius_to_kelvin,
    kelvin_to_celsius,
    per_second_to_daily,
    per_second_to_hourly,
)
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

# Enable logging output as default for the whole package
log.configure()
