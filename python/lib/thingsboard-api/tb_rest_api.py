"""
Base module providing partial support for thingsboard client-side REST API calls.

Dependencies:
- requests : For http POST request
- jwt : JWT decoding

Reference:
- https://thingsboard.io/docs/api/
"""
import math as _math
import socket as _socket
import sys as _sys
from datetime import date, datetime, timedelta

# Dependencies
# import jwt as _jwt
import requests as _requests

# Python2/3 Compatibility
# pylint: disable=consider-using-f-string
if _sys.version_info[0] >= 3:
    long = int  # pylint: disable=invalid-name
try:
    # Python 3+
    # from urllib.parse import quote as _urlquote
    # from urllib.parse import unquote as _urlunquote
    from urllib.parse import urljoin as _urljoin
    from urllib.parse import urlsplit as _urlsplit
except ImportError:
    # Python 2.X
    # from urllib import quote as _urlquote
    # from urllib import unquote as _urlunquote
    from urlparse import urljoin as _urljoin  # type: ignore
    from urlparse import urlsplit as _urlsplit  # type: ignore


class Account():
    """Account class to authenticate with thingsboard server.

    General usage flow is as follows:
    - Create account object with url path to thingsboard server
    - Authenticate account with username and password

    Methods:
    - `set_url(url)`: Modify url used by account thingsboard account.
    - `authenticate(username, password)`: Authenticate user account to get JWT token.
    - `update_token()`: Renews token.
    - `token_expired()`: Checks if token is expired.
    """

    def __init__(self, url):
        # type: (str) -> None
        """
        Constructs all the necessary attributes for the user object.

        Args:
            url (str): Full URL path to connect to thingsboard, including port, \
                must included http(s). i.e. http(s)://host:port
        """
        self._url = None
        """Thingsboard URL, including port if provided."""
        self.__token_info = {"token": None, "refreshToken": None, "exp": 0}
        """Reference to jwt token info (dict[str, str | int])."""
        self.set_url(url)

    @property
    def url(self):
        # type (...) -> str
        """Thingsboard url, including port if provided (`str`, read-only)."""
        return self._url

    @property
    def token(self):
        # type: (...) -> (str | None)
        """Returns the main JWT token for the user (`str`, read-only)."""
        return self.__token_info["token"]

    @property
    def refreshToken(self):  # pylint: disable=invalid-name
        # type: (...) -> (str | None)
        """Returns the JWT refreshToken for the user (`str`, read-only)"""
        return self.__token_info["refreshToken"]

    def set_url(self, url):
        # type (...) -> None
        """Modify url used by Thingsboard account.

        Args:
            url (str): URL to Thingsboard server including port number.

        Raises:
            ValueError: URL does not include http(s).
            gaierror: Socket error.
        """
        url_ = _urlsplit(url)
        if url_.scheme in ("http", "https"):
            # self.url = _urlquote(string=url, safe="/:=?&#")
            self._url = url
        else:
            raise ValueError("URL requires http(s).")

    def authenticate(self, username, password, timeout=3):
        # type: (str, str, int|float|None) -> bool
        """
        Authenticate with thingsboard server to obtain JWT token for the user.

        Args:
            username (str): Username of user for authentication.
            password (str): Password of user for authentication.
            timeout (int | float, Optional): How many seconds to wait for the \
                server to send data before giving up. Defaults to 3.

        Returns:
            bool: True on successfull authentication, False otherwise.
        """
        url_path = _urljoin(self.url, "/api/auth/login")
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        data = {'username': str(username), 'password': str(password)}
        auth_response = _requests.post(url=url_path,
                                       headers=headers,
                                       json=data,
                                       timeout=timeout)
        if auth_response.ok:
            return self.__save_token(auth_response.json())
        return False

    def update_token(self, timeout=3):
        # type: (int|float|None) -> bool
        """Obtain new token using existing refresh token.

        Args:
            timeout (int | float, optional): How many seconds to wait for the \
                server to send data before giving up. Defaults to 3.

        Returns:
            bool: True on successfull update, False otherwise.

        References:
        - https://github.com/thingsboard/thingsboard/issues/840
        """
        url_path = _urljoin(self.url, '/api/auth/token')
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        # The following line may not be needed unsure
        # headers["X-Authorization"] = "Bearer {}".format(self.refreshToken)
        auth_header = {'refreshToken': str(self.refreshToken)}
        auth_response = _requests.post(url=url_path,
                                       headers=headers,
                                       json=auth_header,
                                       timeout=timeout).json()
        if auth_response.ok:
            return self.__save_token(auth_response.json())
        return False

    # def token_expired(self):
    #     """Checks if main jwt token is expired"""
    #     try:
    #         _jwt.decode(jwt=self.__token, verify=False)
    #     except _jwt.ExpiredSignatureError:
    #         return True
    #     else:
    #         return False

    def __save_token(self, jwt):
        # type: (dict) -> bool
        """Saves JSON web token info.

        Returns:
            bool: True: Token saved, False otherwise.
        """
        if isinstance(jwt, dict) and \
                jwt.get("token") is not None:
            self.__token_info["token"] = jwt["token"]
            self.__token_info["refreshToken"] = jwt["refreshToken"]
            return True
        # try:
        #     parsed_token = jwt.decode(jwt, verify=False)
        #     self.__token_info["exp"] = parsed_token["exp"]
        # except jwt.ExpiredSignatureError:
        #     return
        return False


class Device():
    """
    A class to represent the thingsboard device for Thingsboard REST API.

    Attributes:
        account (Account): Account used for device telemetry.
        name (str): Name of device (User given), unrelated to name on thingsboard.
        device_id (str): Device ID of the as used by application.
        keys_ts (list): List of keys from timeseries telemetry used by device.

    Methods:
    - `get_keys_timeseries()`: Get device keys from thingsboard device timeseries.
    - `get_timeseries()`: Get data from thingsboard device telemetry as per REST API.
    """

    def __init__(self, account, name, device_id):
        # type: (Account, str, str) -> None
        """
        Constructs all the necessary attributes for the device object.

        Args:
            account (thingsboard_api.Account): Account used for device telemetry.
            name (str): Name of device (user given).
            device_id (str): Device ID as used by thingsboard.
        """
        # assert isinstance(account, Account)
        self.account = account
        """Reference to account used by device."""
        self.name = name
        """Reference to device name (user given)."""
        self.device_id = device_id
        """Reference to Device ID."""
        self.keys_ts = None
        """Reference to device timeseries keys."""

    def get_keys_timeseries(self, copy=False, timeout=3):
        # type: (bool|None, int|float|None) -> list[str]|bool|None
        """Retrieve timeseries keys belonging to device.

        Args:
            copy (bool, optional): Returns shallow copy of keys.
            timeout (int | float, optional): How many seconds to wait for the \
                server to send data before giving up. Defaults to 3.

        Returns:
            list[str] or False: Timeseries keys if `copy` requested and Successfull.
                False: Request failed. None otherwise.
        """
        url_header = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/DEVICE/{}/keys/timeseries".format(
                self.device_id)
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        response = _requests.get(url_header,
                                 headers=headers,
                                 timeout=timeout)
        if response.ok:
            self.keys_ts = response.json()
            if copy:
                return self.keys_ts.copy()
            return None
        return False

    def get_timeseries(self,
                       startTs,  # type: datetime|date|int|float # pylint: disable=invalid-name
                       endTs,  # type: datetime|date|int|float # pylint: disable=invalid-name
                       keys=None,  # type: tuple|list|str|None
                       limit=50000,  # type: int|None
                       interval=None,  # type: timedelta|int|None
                       agg=None,  # type: str|None
                       tz_offset=0,  # type: timedelta|int|float
                       timeout=10,  # type: int|float|None
                       ):  # type: (...) -> dict[str, list[dict[str, any]]]
        """Retrieves timeseries data from device.

        Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
        is the same as `ts` sent with payload during upload if included.

        Time sample window is exclusive of `startTs` and inclusive of `endTs`
        at millisecond resolution. `(startTs, endTs]`

        `startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00`
        and will exclude the timestamp from the result.


        Args:
            startTs (datetime|date|int|float): Interval start time. \
                    Accepts date object, datetime object or Unix timestamp in milliseconds. \
                    Not inclusive at millisecond resolution. \
                    If `startTs` is `date` type object, time will be set to `00:00:00`.
            endTs (datetime|date|int|float): Interval end time. \
                    Accepts date object, datetime object or Unix timestamp in milliseconds. \
                    Inclusive at millisecond resolution.\
                    If `endTs` is `date` type object, time will be set to `23:59:59.999999`.
            keys (tuple|list|str, optional): Limit data to specified telemetry keys only. \
                    None, will use instance stored `Device().keys` if available. \
                    Defaults to None or Device.
            limit (int, optional): Last (max) number of records to return or \
                    intervals to process, zero and non-positive limit will \
                    use default limit. Defaults to 50000.
            interval (timedelta|int, optional): Aggregation interval in milliseconds.\
                    Also accept timedelta object. Defaults to None.
            agg (str, optional): Aggregation function. \
                    Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
            tz_offset (int|float|timedelta, optional): Time offset in hours to apply to \
                    `startTs` and `endTs`, if the time provided was NOT UTC time. \
                    i.e. for AEST time of +10 from UTC. `tzoffset=10`, \
                    Also accepts timedelta object. Defaults to 0.
            timeout (int | float, optional): How many seconds to wait for the \
                    server to send data before giving up. Defaults to 10.


        Raises:
            ValueError: Invalid "agg" value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT.
            TypeError: Invalid "interval" value.
            ValueError: Invalid "limit" value.
            RuntimeError: "agg" or "interval argument required, if either is used.

        Returns:
            dict{key: list[dict{ts: value}]}: Telemetry data with \
                    telemetry key as dictionary key and value consisting of list \
                    of timeseries and value. None otherwise.


        Examples:
        ```python
        # returns
        {
            'key1': [{'ts': 1657907105161, 'value': '300.0'},
                     {'ts': 1657906205118, 'value': '303.0'}],
            'key2': [{'ts': 1657907105161, 'value': '0.4'},
                     {'ts': 1657906205118, 'value': '0.2'}]
        }

        # NOTE: `ts` when converted to datetime may show an offset from thingsboard web.
        # As the website automatically adjust to browser timezone.
        ```

        http(s)://host:port/api/plugins/telemetry/{entityType}/{entityId}/values/timeseries\
        ?keys=key1,key2,key3&startTs=1479735870785&endTs=1479735871858\
        &interval=60000&limit=100&agg=AVG

        limit set to 50000 same as web. As when limit not provided in api request,\
            it defaults to 100 records.

        References:
        - https://thingsboard.io/docs/user-guide/telemetry/#get-historical-time-series-data-values-for-specific-entity
        - https://github.com/thingsboard/thingsboard/issues/10751
        """
        params = {}  # URL params reference

        # Build "keys" param
        if keys:
            if isinstance(keys, str):
                params["keys"] = keys
            else:
                params["keys"] = ','.join(keys)
        elif self.keys_ts:
            params["keys"] = ','.join(self.keys_ts)

        # Convert date time to millisecond unix timestamp for thingsboard requirement
        SECONDS_2_MILLIS = 1000  # Seconds to Milliseconds factor. # pylint: disable=invalid-name
        if isinstance(startTs, (datetime, date)):
            # datetime is sublcass of date, # pylint: disable-next=unidiomatic-typecheck
            if type(startTs) is date:
                startTs = datetime.combine(startTs, datetime.min.time())
            startTs -= datetime(year=1970, month=1, day=1)
            startTs -= tz_offset if isinstance(tz_offset,
                                               timedelta) else timedelta(hours=tz_offset)
            startTs = startTs.total_seconds() * SECONDS_2_MILLIS
        if isinstance(startTs, float):
            startTs = _math.floor(startTs)
        if startTs:
            params["startTs"] = startTs

        if isinstance(endTs, (datetime, date)):
            # datetime is sublcass of date, # pylint: disable-next=unidiomatic-typecheck
            if type(endTs) is date:
                endTs = datetime.combine(endTs, datetime.max.time())
            endTs -= datetime(year=1970, month=1, day=1)
            endTs -= tz_offset if isinstance(tz_offset,
                                             timedelta) else timedelta(hours=tz_offset)
            endTs = endTs.total_seconds() * SECONDS_2_MILLIS
        if isinstance(endTs, float):
            endTs = _math.ceil(endTs)
        if endTs:
            params["endTs"] = endTs

        # Build "limit" param
        MAX_LIMIT = 50000  # Limit as observed on GUI # pylint: disable=invalid-name
        if isinstance(limit, (float)) or limit is True:
            params["limit"] = round(limit)
        elif limit is None or limit is False:
            params["limit"] = MAX_LIMIT
        elif isinstance(limit, str) and limit.isnumeric():
            params["limit"] = limit if int(limit) > 0 else MAX_LIMIT
            # For py2/py3 Long type, pylint: disable-next=possibly-used-before-assignment
        elif not (isinstance(limit, (int, long)) or (isinstance(limit, str) and limit.isnumeric())):
            raise ValueError("Invalid limit value")
        else:
            params["limit"] = limit if limit > 0 else MAX_LIMIT

        # Build "interval" param
        if interval:
            if not agg:
                raise RuntimeError("\"agg\" argument required")
            if isinstance(interval, timedelta):
                interval = round(interval.total_seconds() * SECONDS_2_MILLIS)
            elif isinstance(interval, float):
                interval = round(interval)
            elif not (isinstance(interval, str) and interval.isnumeric() or
                      (not isinstance(interval, bool) and isinstance(interval, (int, long)))):
                raise TypeError("Invalid interval value")
            params["interval"] = interval

        # build "agg" param
        if agg:
            if not interval:
                raise RuntimeError("\"interval\" argument required")
            if not isinstance(agg, str) or \
                    agg.upper() not in ("MIN", "MAX", "AVG", "SUM", "COUNT"):
                raise ValueError(
                    "Invalid \"agg\" value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT")
            params["agg"] = agg

        base_url = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/DEVICE/{}/values/timeseries".format(
                self.device_id)
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        response = _requests.get(url=base_url,
                                 params=params,
                                 headers=headers,
                                 timeout=timeout)
        if response.ok:
            return response.json()
