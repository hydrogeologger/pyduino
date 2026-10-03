"""This package contains modules and functions to assist with post processing.

Dependencies:
- matplotlib
- numpy
- pandas
"""

# Module Info
__version__ = "0.1.0"

from .pandas_utils import (
    unique_index_levels_only,
    insert_index_level,
    flatten_column_headers,
    swap_index,
)

from .transformation import (
    normalise,
    calculate_delta,
)

from .interpolation import Interpolation

from ._logging import (
    configure_output,
    disable_output,
)
# Enable logging output as default for the whole package
configure_output()
