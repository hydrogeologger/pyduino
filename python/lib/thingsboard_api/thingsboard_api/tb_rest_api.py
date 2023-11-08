"""
This module provides partial support for thingsboard client-side REST API calls \
    using requests calls.

Reference: https://thingsboard.io/docs/api/

Dependencies:
- requests : For http POST request
- jwt : JWT decoding
"""

# Dependencies
import datetime
import requests
# import jwt


class Account():
    """Account class to authenticate with thingsboard server.

    General usage flow is as follows:
    - Create account object with url path to thingsboard server
    - Authenticate account with username and password

    Attributes:
        url (str): URL for thingsboard

    Properties:
        token (str): Thingsboard JWT token
        refreshToken (str): Thingsboard JWT refresh Token

    Methods:
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
            url (str): Full URL path to connect to thingsboard, must included http/https
        """
        if url.startswith("http"):
            self.url = url
        else:
            self.url = "http://" + url
        self.__token_info = {"token": None, "refreshToken": None, "exp": 0}

    @property
    def token(self):
        # type: () -> str | None
        """Returns the main JWT token for the user"""
        return self.__token_info["token"]

    @property
    def refreshToken(self): # pylint: disable=invalid-name
        # type: () -> str | None
        """Returns the JWT refreshToken for the user"""
        return self.__token_info["refreshToken"]

    def authenticate(self, username, password):
        # type: (str, str) -> None
        """
        Authenticate with thingsboard server to obtain JWT token for the user.

        Args:
            username (str): Username of user for authentication
            password (str): Password of user for authentication
        """
        url_path = self.url + '/api/auth/login'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        auth_header = {'username': str(username), 'password': str(password)}
        auth_response = requests.post(url=url_path, headers=headers,
                json=auth_header, timeout=3).json()
        self.__save_token(auth_response)

    def update_token(self):
        # type: () -> None
        """
        Obtain new token using existing refresh token
        https://github.com/thingsboard/thingsboard/issues/840
        """
        url_path = self.url + '/api/auth/token'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        # The following line may not be needed unsure
        headers["X-Authorization"] = "Bearer " + self.refreshToken
        auth_header = {'refreshToken': str(self.refreshToken)}
        auth_response = requests.post(url=url_path, headers=headers,
                json=auth_header, timeout=3).json()
        self.__save_token(auth_response)

    # def token_expired(self):
    #     """Checks if main jwt token is expired"""
    #     try:
    #         jwt.decode(jwt=self.__token, verify=False)
    #     except jwt.ExpiredSignatureError:
    #         return True
    #     else:
    #         return False

    def __save_token(self, jwt):
        # type: (dict) -> None
        """Saves JSON web token info."""
        if isinstance(jwt, dict) and \
                jwt.get("token") is not None:
            self.__token_info["token"] = jwt["token"]
            self.__token_info["refreshToken"] = jwt["refreshToken"]
        # try:
        #     parsed_token = jwt.decode(jwt, verify=False)
        #     self.__token_info["exp"] = parsed_token["exp"]
        # except jwt.ExpiredSignatureError:
        #     return


class Device():
    """
    A class to represent the thingsboard device for Thingsboard REST API.

    Attributes:
        account (Account): Account used for device telemetry
        name (str): Name of device (User given)
        device_id (str): Device ID of the device
        keys (list): List of keys from thingsboard telemetry

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
            account (thingsboard_api.Account): Account used for device telemetry
            name (str): Name of device (user given)
            device_id (str): Device ID as used by thingsboard
        """
        # assert isinstance(account, Account)
        self.account = account
        self.name = name
        self.device_id = device_id
        self.keys = None


    def get_keys(self):
        # type: () -> list[str]
        """Retrieve and returns telemetry keys belonging to device."""
        url_header = self.account.url + \
                '/api/plugins/telemetry/DEVICE/' + str(self.device_id) + \
                '/keys/timeseries'
        headers = {'Content-Type': 'application/json',
                   'X-Authorization':'bearer '+ str(self.account.token)}
        self.keys = requests.get(url_header, headers=headers, timeout=3).json()
        return self.keys

    # pylint: disable-next=invalid-name, too-many-arguments
    def get_data(self, startTs, # type: datetime.datetime|int|float
                 endTs, # type: datetime.datetime|int|float # pylint: disable=invalid-name
                 keys=None, # type: tuple|list|str|None
                 limit=None, # type: int|None
                 interval=None, # type: datetime.timedelta|int|None
                 agg=None, # type: str|None
                 tz_offset=0 # type: float|int
                 ): # type: (...) -> None
        """
        Retrieves timeseries data from device.
        https://thingsboard.io/docs/user-guide/telemetry#data-query-api

        Args:
            startTs (datetime|int|float): Start of time interval. \
                    Either datetime object or Unix timestamp in milliseconds.
            endTs (datetime|int|float): End of time interval, not inclusive.\
                    Either datetime object or Unix timestamp in milliseconds.
            keys (tuple|list|str, optional): Limit data to specified telemetry keys only. \
                    Defaults to None.
            limit (int, optional): Max amount of data points to return. Defaults to None.
            interval (timedelta|int, optional): Aggregation interval in milliseconds.\
                    Also accept timedelta object. Defaults to None.
            agg (str, optional): Aggregation function. \
                    Accepts (MIN, MAX, AVG, SUM, COUNT, NONE). Defaults to None.
            tz_offset (float, optional): Timezone offset in hours. Defaults to 0.

        Raises:
            ValueError: List of keys not specified.
            ValueError: AGG function not one of MIN, MAX, AVG, SUM, COUNT

        Returns:
            json object: Dictionary of telemetry data with telemetry key as dictionary \
                    key and value consisting list of timeseries and value. \
                    dict{key : list[ts, value]}
        """
        if keys:
            if isinstance(keys, str):
                keys_string = keys
            else:
                keys_string = ','.join(keys)
        elif self.keys:
            keys_string = ','.join(self.keys)
        else:
            raise ValueError("keys is empty")

        if agg and agg.upper() not in ("MIN", "MAX", "AVG", "SUM", "COUNT"):
            raise ValueError("agg is not one of MIN, MAX, AVG, SUM, COUNT")

        # Convert date time to millisecond unix timestamp for thingsboard requirement
        SECONDS_2_MILLIS = 1000 # seconds to milliseconds conversion factor. pylint: disable=invalid-name
        if isinstance(startTs, datetime.datetime):
            startTs = int((startTs - datetime.datetime(year=1970, month=1, day=1) + \
                    datetime.timedelta(hours=tz_offset)).total_seconds()) * SECONDS_2_MILLIS
        elif isinstance(startTs, float):
            startTs = round(startTs)
        if isinstance(endTs, datetime.datetime):
            endTs = int((endTs - datetime.datetime(year=1970, month=1, day=1) + \
                    datetime.timedelta(hours=tz_offset)).total_seconds()) * SECONDS_2_MILLIS
        elif isinstance(endTs, float):
            endTs = round(endTs)

        url_header = self.account.url + \
                '/api/plugins/telemetry/DEVICE/' + str(self.device_id) + \
                '/values/timeseries?' + \
                'keys=' + keys_string + \
                '&startTs=' + str(startTs) + \
                '&endTs=' + str(endTs)
        if interval:
            if isinstance(interval, datetime.timedelta):
                interval = round(interval.total_seconds()) * SECONDS_2_MILLIS
            elif isinstance(interval, float):
                interval = round(interval)
            url_header = url_header + '&interval=' + str(interval)
        if agg:
            url_header = url_header + '&agg=' + str(agg)
        if limit:
            url_header += '&limit=' + str(limit)
        headers = {'Content-Type': 'application/json',
                   'X-Authorization': 'bearer '+ str(self.account.token)}
        return requests.get(url_header, headers=headers, timeout=3).json()
