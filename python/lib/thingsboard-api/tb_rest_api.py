"""
Base module providing partial support for thingsboard client-side REST API calls.

Dependencies:
- requests : For http POST request
- jwt : JWT decoding

Reference:
- https://thingsboard.io/docs/api/
"""
import math as _math
import sys as _sys
from collections import defaultdict as _defaultdict
from datetime import date, datetime, timedelta
from typing import Any as _Any
from typing import Union as _Union

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


def _process_ms_from_epoch(ts, tz_offset=0):
    # type: (datetime|date|int|float|None, int|float|timedelta) -> int|None
    """Calculate datetime value to milliseconds from epoch.

    Convert date time to millisecond unix timestamp

    Args:
        ts (datetime|date|int|float|None): Naive Datetime or date object or
            Unix timestamp in milliseconds.
        tz_offset (int|float|timedelta, optional): Time offset in hours to apply to
            `startTs` and `endTs`, if the time provided was NOT UTC time.
            i.e. for AEST time of +10 from UTC. `tzoffset=10`,
            Also accepts timedelta object. Defaults to 0.

    Returns:
        int|None: Unix time in milliseconds since epoch time. Returns None if `ts`
            was None.
    """
    SECONDS_2_MILLIS = 1000  # Seconds to Milliseconds factor. # pylint: disable=invalid-name
    if isinstance(ts, (datetime, date)):
        # datetime is sublcass of date, # pylint: disable-next=unidiomatic-typecheck
        if type(ts) is date:
            ts = datetime.combine(ts, datetime.max.time())
        ts = (ts - datetime(year=1970, month=1, day=1)).total_seconds()
        ts -= (tz_offset if isinstance(tz_offset, timedelta)
               else timedelta(hours=tz_offset)).total_seconds()
        ts *= SECONDS_2_MILLIS
    if isinstance(ts, float):
        ts = _math.ceil(ts)
    return ts


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
            url (str): Full URL path to connect to thingsboard, including port,
                must included http(s). i.e. http(s)://host:port
        """
        self._url = ""
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
            timeout (int | float, Optional): How many seconds to wait for the
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
            timeout (int | float, optional): How many seconds to wait for the
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
        device_id (str): Device ID of the as used by application.
        name (str): Name of device (User given), unrelated to name on thingsboard.
        keys_ts (list): List of keys from timeseries telemetry used by device.

    Methods:
    - `get_keys_timeseries()`: Get device keys from thingsboard device timeseries.
    - `get_timeseries()`: Get data from thingsboard device telemetry as per REST API.
    """

    def __init__(self, account, device_id, name):
        # type: (Account, str, str) -> None
        """
        Constructs all the necessary attributes for the device object.

        Args:
            account (thingsboard_api.Account): Account used for device telemetry.
            device_id (str): Device ID as used by thingsboard.
            name (str): Name of device (user given).
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
            timeout (int | float, optional): How many seconds to wait for the
                server to send data before giving up. Defaults to 3.

        Returns:
            list[str]|False|None: On successfull key retrieval, will return
                None if `copy=False` or a shallow copy list of keys
                if `copy=True`. Returns False if retrieval failed.

        API Endpoint:
        > GET /api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries
        """
        url_header = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/{entityType}/{entityId}/keys/timeseries".format(
                entityType="DEVICE",
                entityId=self.device_id
            )
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
                       startTs=None,  # type: datetime|date|int|float|None # pylint: disable=invalid-name
                       endTs=None,  # type: datetime|date|int|float|None # pylint: disable=invalid-name
                       keys=None,  # type: tuple|list|str|None
                       limit=50000,  # type: int|None
                       interval=None,  # type: timedelta|int|None
                       agg=None,  # type: str|None
                       tz_offset=0,  # type: timedelta|int|float
                       useStrictDataTypes=True,  # type: bool # type: pylint: disable=invalid-name
                       timeout=30,  # type: int|float|None
                       ):  # type: (...) -> dict[str, list[dict[str, _Any]]]|None
        """Retrieves timeseries data from device.

        Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
        is the same as `ts` sent with payload during upload if included.

        Time sample window is exclusive of `startTs` and inclusive of `endTs`
        at millisecond resolution. `(startTs, endTs]`

        `startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00`
        and will values with exact same timestamp is exclude from the result.

        If no aggregation or time interval given, will return latest timseries values.

        Args:
            startTs (datetime|date|int|float): Interval start time.
                    Accepts date object, datetime object or Unix timestamp in milliseconds.
                    Not inclusive at millisecond resolution.
                    If `startTs` is `date` type object, time will be set to `00:00:00`.
            endTs (datetime|date|int|float): Interval end time.
                    Accepts date object, datetime object or Unix timestamp in milliseconds.
                    Inclusive at millisecond resolution.
                    If `endTs` is `date` type object, time will be set to `23:59:59.999999`.
            keys (tuple|list|str, optional): Limit data to specified telemetry keys only.
                    None, will use instance stored `Device().keys_ts` if available.
                    Defaults to None or Device.
            limit (int, optional): Last (max) number of records to return or
                    intervals to process, zero and non-positive limit will
                    use default limit. Used only when `agg` parameter is set to 'NONE'.
                    Defaults to 50000.
            interval (timedelta|int, optional): Aggregation interval in milliseconds.
                    Also accept timedelta object. Defaults to None.
            agg (str, optional): Aggregation function.
                    Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
            tz_offset (int|float|timedelta, optional): Time offset in hours to apply to
                    `startTs` and `endTs`, if the time provided was NOT UTC time.
                    i.e. for AEST time of +10 from UTC. `tzoffset=10`,
                    Also accepts timedelta object. Defaults to 0.
            timeout (int | float, optional): How many seconds to wait for the
                    server to send data before giving up. Defaults to 30.
            useStrictDataTypes (bool, optional): Enables/disables conversion of telemetry
                    values to strings. Set `useStrictDataTypes=true` to disable value
                    conversion to string. Defaults to True.

        Raises:
            ValueError: Invalid `agg` value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT.
            TypeError: Invalid `interval` value.
            ValueError: Invalid `limit` value.
            RuntimeError: Aggrigation request requires `agg`, `interval`, `startTs` and `endTs`.

        Returns:
            dict|None: Returns telemetry data with with the format
                dict{key: list[dict{ts: value}]} telemetry key as dictionary key
                and value consisting of a list of timeseries and value. None otherwise.

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

        Limit set to 50000 same as web. As when limit not provided in api request,
        it defaults to 100 records. Used when `agg` parameter is `none`.

        References:
        - https://thingsboard.io/docs/user-guide/telemetry/#get-historical-time-series-data-values-for-specific-entity
        - https://github.com/thingsboard/thingsboard/issues/10751

        API Endpoint:
        > GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries{?keys,useStrictDataTypes}

        > GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries{?keys,startTs,endTs,intervalType,interval,timeZone,limit,agg,orderBy,useStrictDataTypes}

        > GET /api/plugins/telemetry/{entityType}/{entityId}/values/timeseries?keys=key1,key2,key3&startTs=1479735870785&endTs=1479735871858&interval=60000&limit=100&agg=AVG
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
        startTs = _process_ms_from_epoch(ts=startTs, tz_offset=tz_offset)
        if startTs is not None:
            params["startTs"] = startTs

        endTs = _process_ms_from_epoch(ts=endTs, tz_offset=tz_offset)
        if endTs is not None:
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
        SECONDS_2_MILLIS = 1000  # Seconds to Milliseconds factor. # pylint: disable=invalid-name
        if interval:
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
            if not isinstance(agg, str) or \
                    agg.upper() not in ("MIN", "MAX", "AVG", "SUM", "COUNT"):
                raise ValueError(
                    "Invalid \"agg\" value, Only Accepts one of MIN, MAX, AVG, SUM, COUNT")
            params["agg"] = agg

        if ((any((interval, agg)) and not all((startTs, endTs))) or bool(interval) ^ bool(agg)):
            raise RuntimeError(
                "One or more arguments `agg`, `interval`, `startTs` or `endTs` is missing.")

        if useStrictDataTypes:
            params["useStrictDataTypes"] = True

        base_url = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/{entityType}/{entityId}/values/timeseries".format(
                entityType="DEVICE",
                entityId=self.device_id,
            )
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        response = _requests.get(url=base_url,
                                 params=params,
                                 headers=headers,
                                 timeout=timeout)
        if response.ok:
            return response.json()

    def update_timeseries(self, data, timeout=10):
        # type: (_Union[dict[str, _Any], list[dict[str, _Any]]], int|float|None) -> bool
        """
        Update thingsboard timeseries telemetry (time-series) data.

        Warning:
            Does NOT do any data structure validation.

        Data in JSON Format (officially supported):
        ```json
        //# Without timestamps (server assigns current time):
        {"temperature": 22.5, "humidity": 58}

        //# With explicit timestamps (milliseconds since epoch):
        //# Single point:
        {"ts": 1730457600000, "values": {"temperature": 22.3, "humidity": 57}}
        //# Multiple points (array):
        [
            {"ts": 1730457600000, "values": {"temperature": 22.3, "humidity": 57}},
            {"ts": 1730461200000, "values": {"temperature": 22.7, "humidity": 59}}
        ]
        ```

        Args:
            data (dict): Telemetry data, either a simple dict of key-value pairs,
                  a dict with "ts" and "values", or a list of timestamped dicts.
            timeout (int | float, optional): How many seconds to wait for the
                    server to send data before giving up. Defaults to 10.

        Returns:
            bool: Returns true if update was successfull, false otherwise.

        API Endpoint:
        > POST /api/plugins/telemetry/DEVICE/{deviceId}/timeseries/{scope}
        """
        base_url = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/{entityType}/{entityId}/timeseries/{scope}".format(
                entityType="DEVICE",
                entityId=self.device_id,
                scope="SERVER_SCOPE"
            )
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        response = _requests.post(url=base_url,
                                  headers=headers,
                                  json=data,
                                  timeout=timeout)
        if response.ok:
            return True
        return False

    def delete_timeseries(self,
                          keys,  # type: tuple|list|str
                          startTs=None,  # type: datetime|date|int|float|None # pylint: disable=invalid-name
                          endTs=None,  # type: datetime|date|int|float|None # pylint: disable=invalid-name
                          deleteLatest=False,  # type: bool|None # pylint: disable=invalid-name
                          rewriteLatestIfDeleted=True,  # type: bool|None # pylint: disable=invalid-name
                          deleteAllDataForKeys=False,  # type: bool|None # pylint: disable=invalid-name
                          tz_offset=0,  # type: timedelta|int|float
                          timeout=10,  # type: int|float|None
                          ):  # type: (...) -> bool
        """Delete timeseries data from device.

        Timestamp `ts` used by thingsboard is UTC time, and the retrieved `ts`
        is the same as `ts` sent with payload during upload if included.

        Time sample window is exclusive of `startTs` and inclusive of `endTs`
        at millisecond resolution. `(startTs, endTs]`

        `startTs` date object `2024-05-01` will be parsed as `2024-05-01 00:00:00.00`
        and will values with exact same timestamp is exclude from the result.

        Args:
            keys (tuple|list|str): Limit data to specified telemetry keys only.
                    None, will use instance stored `Device().keys` if available.
                    Defaults to None or Device.
            startTs (datetime|date|int|float, optional): Interval start time.
                    Accepts date object, datetime object or Unix timestamp in milliseconds.
                    Not inclusive at millisecond resolution.
                    If `startTs` is `date` type object, time will be set to `00:00:00`.
            endTs (datetime|date|int|float, optional): Interval end time.
                    Accepts date object, datetime object or Unix timestamp in milliseconds.
                    Inclusive at millisecond resolution.
                    If `endTs` is `date` type object, time will be set to `23:59:59.999999`.
            deleteLatest (bool, optional): Latest telemetry can be removed, otherwise latest
                    value will not be removed. Defaults to False.
            rewriteLatestIfDeleted (bool, optional): Latest telemetry table will be rewritten
                    in case that current latest value was removed. Defaults to True.
            deleteAllDataForKeys (bool, optional): Flag to specificy if all data should
                    be deleted for selected keys or only data within specified time range.
                    Defaults to False.
            tz_offset (int|float|timedelta, optional): Time offset in hours to apply to
                    `startTs` and `endTs`, if the time provided was NOT UTC time.
                    i.e. for AEST time of +10 from UTC. `tzoffset=10`,
                    Also accepts timedelta object. Defaults to 0.
            timeout (int | float, optional): How many seconds to wait for the
                    server to send data before giving up. Defaults to 10.

        Returns:
            bool: Returns true if delete was successfull, false otherwise.

        API Endpoint:
        > DELETE /api/plugins/telemetry/{entityType}/{entityId}/timeseries/delete{?keys,deleteAllDataForKeys,startTs,endTs,deleteLatest,rewriteLatestIfDeleted}
        """
        params = {}  # URL params reference

        # Build "keys" param
        if keys:
            if isinstance(keys, str):
                params["keys"] = keys
            else:
                params["keys"] = ','.join(keys)

        # Convert date time to millisecond unix timestamp for thingsboard requirement
        startTs = _process_ms_from_epoch(ts=startTs, tz_offset=tz_offset)
        if startTs is not None:
            params["startTs"] = startTs

        endTs = _process_ms_from_epoch(ts=endTs, tz_offset=tz_offset)
        if endTs is not None:
            params["endTs"] = endTs

        if deleteAllDataForKeys:
            params["deleteAllDataForKeys"] = True

        if deleteLatest:
            params["deleteLatest"] = True

        if rewriteLatestIfDeleted:
            params["rewriteLatestIfDeleted"] = True

        base_url = _urljoin(
            self.account.url,
            "/api/plugins/telemetry/{entityType}/{entityId}/timeseries/delete".format(
                entityType="DEVICE",
                entityId=self.device_id
            )
        )
        headers = {"Content-Type": "application/json",
                   "X-Authorization": "Bearer {}".format(self.account.token)}
        response = _requests.delete(url=base_url,
                                    params=params,
                                    headers=headers,
                                    timeout=timeout)
        if response.ok:
            return True
        return False


def group_timeseries_by_ts(data):
    # type: (dict) -> list[dict]
    """Groups timestamped key-value readings into a list of records by timestamp.

    This function takes a dictionary where each key maps to a list of readings
    with timestamps. Readings with the same timestamp across different keys
    are merged into a single record.

    Missing keys for a timestamp are omitted. The resulting list is sorted by timestamp.

    Args:
        data (dict): A dictionary of the form:
            ```python
            {
                key1: [{"ts": int, "value": str}, ...],
                key2: [{"ts": int, "value": str}, ...],
                ...
            }
            ```

    Returns:
        list[dict]: A list of records, each with the structure:
            ```python
            {
                "ts": <timestamp>,
                "values": {
                    key1: <value>,
                    key2: <value>,
                    ...
                }
            }
            ```

    Example:
        ```python
        data = {
            "temperature": [{"ts": 1000, "value": "25.5"}, {"ts": 2000, "value": "26.0"}],
            "humidity": [{"ts": 1000, "value": "80"}]
        }
        group_timeseries_by_ts(data)
        [
            {"ts": 1000, "values": {"temperature": 25.5, "humidity": 80.0}},
            {"ts": 2000, "values": {"temperature": 26.0}}
        ]
        ```
    """
    grouped = _defaultdict(dict)

    # Group readings by timestamp
    for key, readings in data.items():
        for r in readings:
            ts = r["ts"]
            value = r["value"]

            # Convert numeric strings to float if possible
            # try:
            #     value = float(value)
            # except (ValueError, TypeError):
            #     pass

            grouped[ts][key] = value

    # Convert grouped data into list format
    result = [{"ts": ts, "values": values} for ts, values in grouped.items()]

    # Sort chronologically by timestamp
    result.sort(key=lambda x: x["ts"])

    return result
