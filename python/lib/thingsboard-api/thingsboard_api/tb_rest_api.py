"""
This module provides partial support for thingsboard client-side REST API calls.

Reference: https://thingsboard.io/docs/api/

Dependencies:
- requests : For http POST request
- jwt : JWT decoding
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
    - `set_url(url)`: \
            Modify url used by account thingsboard account.
    - `authenticate(username, password)`: \
            Authenticate user account to get JWT token.
    - `update_token()`: \
            Renews token.
    - `token_expired()`: \
            Checks if token is expired.
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

    def authenticate(self, username, password):
        # type: (str, str) -> bool
        """
        Authenticate with thingsboard server to obtain JWT token for the user.

        Args:
            username (str): Username of user for authentication.
            password (str): Password of user for authentication.

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
                                       timeout=3)
        if auth_response.ok:
            return self.__save_token(auth_response.json())
        return False

    def update_token(self):
        # type: (...) -> bool
        """
        Obtain new token using existing refresh token.
        https://github.com/thingsboard/thingsboard/issues/840

        Returns:
            bool: True on successfull update, False otherwise.
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
                                       timeout=3).json()
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
        name (str): Name of device (User given).
        device_id (str): Device ID of the as used by application.
        keys (list): List of keys from thingsboard telemetry.

    Methods:
    - `get_keys()`: \
            Get device keys from thingsboard device telemetry
    - `get_data()`: \
            Get data from thingsboard device telemetry as per REST API
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
        self.keys = None
        """Reference to device telemetry keys."""

    def get_keys(self):
        # type: () -> list[str]
        """Retrieve and returns telemetry keys belonging to device."""
        url_header = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/DEVICE/{}/keys/timeseries".format(
                self.device_id)
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        self.keys = _requests.get(url_header,
                                  headers=headers,
                                  timeout=3).json()
        return self.keys

    def get_data(self,
                 startTs,  # type: datetime|date|int|float # pylint: disable=invalid-name
                 endTs,  # type: datetime|date|int|float # pylint: disable=invalid-name
                 keys=None,  # type: tuple|list|str|None
                 limit=50000,  # type: int|None
                 interval=None,  # type: timedelta|int|None
                 agg=None,  # type: str|None
                 tz_offset=0  # type: timedelta|int|float
                 ):  # type: (...) -> dict[str, list[dict[str, any]]]
        """Retrieves timeseries data from device.

        Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
        is the same as `ts` sent with payload during upload if included.

        Time sample window is exclusive of `startTs` and inclusive of `endTs`,


        Args:
            startTs (datetime|date|int|float): Interval start time, Not inclusive. \
                    Accepts either datetime object or Unix timestamp in milliseconds. \
                    If `startTs` is `date` type object, time will be set to `0:0`.
            endTs (datetime|date|int|float): Interval end time, inclusive.\
                    Accepts either datetime object or Unix timestamp in milliseconds. \
                    If `endTs` is `date` type object, time will be set to `23:59`.
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

        Raises:
            ValueError: Invalid "agg" value, not one of MIN, MAX, AVG, SUM, COUNT.
            ValueError: Invalid "interval" value.
            ValueError: Invalid "limit" value.

        Returns:
            json object: Dictionary of telemetry data with telemetry key as dictionary \
                    key and value consisting list of timeseries and value. \
                    dict{key: list[dict{ts: value}]}

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
            https://thingsboard.io/docs/user-guide/telemetry/#get-historical-time-series-data-values-for-specific-entity
            https://github.com/thingsboard/thingsboard/issues/10751
        """
        params = {}  # URL params reference

        # Build "keys" param
        if keys:
            if isinstance(keys, str):
                params["keys"] = keys
            else:
                params["keys"] = ','.join(keys)
        elif self.keys:
            params["keys"] = ','.join(self.keys)

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
            if isinstance(interval, timedelta):
                interval = round(interval.total_seconds() * SECONDS_2_MILLIS)
            elif isinstance(interval, float):
                interval = round(interval)
            elif (isinstance(interval, str) and not interval.isnumeric()) or \
                    isinstance(interval, bool) or not isinstance(interval, (int, long)):
                raise ValueError("Invalid interval value")
            params["interval"] = interval

        # build "agg" param
        if agg:
            if not isinstance(agg, str) or \
                    agg.upper() not in ("MIN", "MAX", "AVG", "SUM", "COUNT"):
                raise ValueError(
                    "Invalid \"agg\" value, not one of MIN, MAX, AVG, SUM, COUNT")
            params["agg"] = agg

        base_url = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/DEVICE/{}/values/timeseries".format(
                self.device_id)
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        return _requests.get(url=base_url,
                             params=params,
                             headers=headers,
                             timeout=3).json()
