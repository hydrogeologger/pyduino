"""Common utility and shared resources for the postprocess.sources subpackage."""

__all__ = [
    "advance_one_month",
    "haversine_distance",
    "round_to_nearest_05",
    "URLBuilder",
]

import calendar as _calendar
from math import (
    atan2 as _atan2,
    cos as _cos,
    radians as _radians,
    sin as _sin,
    sqrt as _sqrt,
)
from typing import TYPE_CHECKING

try:
    # Python 3+
    from urllib.parse import urljoin as _urljoin
except ImportError:
    # Python 2.X
    from urlparse import (  # pyright: ignore[reportMissingImports]
        urljoin as _urljoin,
    )

from .types import Coordinates

if TYPE_CHECKING:
    from datetime import (
        date,
        datetime,
    )
    from typing import Tuple

# pylint: disable=consider-using-f-string


def haversine_distance(coord1, coord2, radius=6371.0):
    # type: (Tuple[float, float], Tuple[float, float], float) -> float
    """Computes great-circle distance between two geographic coordinates.

    Applies the Haversine formula to find the shortest spherical distance between
    points. Converts inputs from decimal degrees to radians, validates bounds, 
    and scales the angular separation by the specified planetary radius.

    Args:
        coord1 (tuple): Starting point as (latitude, longitude) coordinate pair in decimal degrees.
        coord2 (tuple): Ending point as (latitude, longitude) coordinate pair in decimal degrees.
        radius (float, Optional): Sphere radius. Defaults to 6371.0 (Earth kilometers).

    Returns:
        float: Great-circle distance in the same unit as radius.

    TypeError: Coordinates is not a tuple or either coordinate is not an
        integer or float.
    ValueError: Coordinates does not contain exactly two values or either
        coordinate is outside its valid range latitudes exceed [-90, 90] or
        longitudes exceed [-180, 180].
    """
    # Validate coordinates
    Coordinates.validate_decimal_degree(coord1)
    Coordinates.validate_decimal_degree(coord2)

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # Convert degrees to radians
    lat1 = _radians(lat1)
    lon1 = _radians(lon1)
    lat2 = _radians(lat2)
    lon2 = _radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        _sin(dlat / 2) ** 2
        + _cos(lat1) * _cos(lat2) * _sin(dlon / 2) ** 2
    )

    # pylint: disable-next=invalid-name
    if radius is None:
        radius = 6371.0  # Earth radius in kilometres.
    c = 2 * _atan2(_sqrt(a), _sqrt(1 - a))
    return radius * c


def round_to_nearest_05(x):
    """Round value to nearest 0.05."""
    return round(x * 20) / 20


def advance_one_month(dt):
    # type: (date|datetime) -> date|datetime
    """Advance a date or datetime by one calendar month, clamping to month end."""
    if dt.month == 12:
        year = dt.year + 1
        month = 1
    else:
        year = dt.year
        month = dt.month + 1
    day = min(dt.day, _calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def generate_monthly_dates(start_date, end_date, end_date_behaviour="exclude"):
    # type: (date|datetime, date|datetime, str) -> list[date|datetime]
    """Generate monthly dates while they are less than or equal to end date,
    preserving the start date's day when possible.

    Args:
        start_date (date | datetime): The date or datetime to start generating
            from. Must be the same type as ``end_date``.
        end_date (date | datetime): The date or datetime to stop generating at.
            Must be the same type as ``start_date``.
        end_date_behaviour (str, optional): Controls how an ``end_date`` that does
            not fall on the monthly sequence is handled. Defaults to ``"exclude"``.
            - ``"exclude"``: Do not include ``end_date``.
            - ``"unique_month"``: Include ``end_date`` if its month is not already
            represented.
            - ``"append"``: Always include ``end_date``.

    Returns:
        list[date | datetime]: Dates from ``start_date`` through ``end_date``,
            according to ``end_date_behaviour``.

    Raises:
        ValueError: If ``end_date_behaviour`` is not one of ``"exclude"``,
            ``"unique_month"``, or ``"append"``.
    """
    valid_behaviours = {"exclude", "unique_month", "append"}
    if end_date_behaviour not in valid_behaviours:
        raise ValueError(
            "`end_date_behaviour` must be `exclude`, "
            "`unique_month`, or `append`"
        )
    dates = []
    current_date = start_date
    original_day = start_date.day

    while current_date <= end_date:
        dates.append(current_date)
        next_date = advance_one_month(current_date)

        if original_day > next_date.day:
            days_in_month = _calendar.monthrange(
                next_date.year, next_date.month
            )[1]
            next_date = next_date.replace(day=min(original_day, days_in_month))

        current_date = next_date

    if dates[-1] != end_date:
        if end_date_behaviour == "unique_month":
            last_date = dates[-1]
            if (last_date.year, last_date.month) != (
                end_date.year,
                end_date.month,
            ):
                dates.append(end_date)

        elif end_date_behaviour == "append":
            dates.append(end_date)
    return dates


class URLBuilder(object):
    """A fluent builder for incrementally constructing well-formed web URLs."""

    def __init__(self, domain, subdomain="", path="", scheme="https"):
        # type: (str, str, str, str) -> None
        """Initialise a URLBuilder instance.

        Args:
            domain (str): Target host or domain.
            subdomain (str, optional): Target subdomain.
                Defaults to None.
            path (str, optional): Base url path.
            scheme (str, optional): url scheme. i.e. `ftp` or `http`
                Defaults to `https`.
        """
        self._scheme = scheme.lower().rstrip("://:")
        self._base_subdomain = subdomain.strip(".")
        self._domain = domain.strip("/")
        self._base_path = path.lstrip("/")

    @property
    def netloc(self):  # type: (...) -> str
        """Returns URL Net location."""
        return self._netloc(self._base_subdomain, self._domain)

    @property
    def origin(self):  # type: (...) -> str
        """Return the origin (scheme + netloc)."""
        return "{}://{}".format(self._scheme, self.netloc)

    @property
    def base_url(self):  # type: (...) -> str
        """Return the full URL by joining base URL and base path."""
        return _urljoin(self.origin, self._base_path)

    def resolve(self, path):  # type (...) -> str
        """Resolve a path relative to the configured base URL."""
        return _urljoin(self.base_url.rstrip("/") + "/", path.lstrip("/"))

    def resolve_root(self, path):  # type: (...) -> str
        """Resolve a path relative to the configured URL origin, ignoring the base path."""
        return _urljoin(self.origin, "/" + path.lstrip("/"))

    def resolve_subdomain(self, subdomain, path=""):  # type: (...) -> str
        """Resolve a path relative to the specified subdomain and configured base path."""
        origin = self._origin_for_subdomain(subdomain)
        base_url = _urljoin(origin, self._base_path)
        return _urljoin(base_url.rstrip("/") + "/", path.lstrip("/"))

    def resolve_root_subdomain(self, subdomain, path=""):  # type: (...) -> str
        """Resolve a path relative to the specified subdomain, ignoring the configured base path."""
        return _urljoin(self._origin_for_subdomain(subdomain), "/" + path.lstrip("/"))

    def _origin_for_subdomain(self, subdomain):  # type: (...) -> str
        """Return the origin for a specified subdomain."""
        return "{}://{}".format(
            self._scheme,
            self._netloc(subdomain.strip("."), self._domain)
        )

    @staticmethod
    def _netloc(subdomain, domain):  # type: (...) -> str
        """Private helper to generate netloc"""
        return ("{}.{}".format(subdomain, domain) if subdomain else domain)
