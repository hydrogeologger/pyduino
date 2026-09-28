"""Access historical climate and weather observations from Australian
Bureau of Meteorology data services.

Modules:
    cdio: Client and tools for fetching daily weather observations.
    ftp: Client and tools for fetching daily weather observations via FTP.
    types: Data structures, records, and base classes for stations.

Examples:
    To use the FTP client to fetch daily weather observations:

        >>> from postprocess.sources import bom
        >>> client = bom.ftp.DailyWeatherObservations()
        >>> client.set_station(94653)
        >>> df = client.load_observations(start_date, end_date)

    To work with station records and metadata classes:

        >>> from postprocess.sources import bom
        >>> station = bom.types.BOMStationBase(
        ...     station_id=94653,
        ...     name="Melbourne Regional Office",
        ...     latitude=-37.8136,
        ...     longitude=144.9631,
        ...     state="VIC",
        ...     elevation_m=31.4,
        ... )
        >>> print(station.name)
        Melbourne Regional Office

References:
- https://www.bom.gov.au/catalogue/data-feeds.shtml
"""

__all__ = [
    "types",
    "cdio",
    "ftp",
]

from . import types
from . import cdio
from . import ftp
