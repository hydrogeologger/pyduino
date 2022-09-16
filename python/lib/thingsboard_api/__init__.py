#!/usr/bin/env python
"""
This module provides the server-side API calls from wrapper functions.

Dependencies:
-------------
    requests : For http POST request
    jwt : JWT decoding
    constants : Constants conversion module
"""

# Module Info
__version__ = "1.0"

# Dependencies
import datetime
import requests
# import jwt


class Account(object):
    """
    A class to represent the user account for Thingsboard REST API.

    ...

    Attributes
    ----------
    url : str
        URL for thingsboard

    Methods
    -------
    authenticate(username, password):
        Authenticate user account to get JWT token
    update_token():
        Retrieves a new token
    token():
        Returns the current active or expired token
    refreshToken():
        Returns the token used for requesting new token
    token_isexpired():
        Returns True/False if token is expired
    """

    def __init__(self, url):
        """
        Constructs all the necessary attributes for the user object.

        Parameters
        ----------
            url : str
                Full URL path to connect to thingsboard, must included http/https
        """
        if url.startswith("http"):
            self.url = url
        else:
            self.url = "http://" + url
        self.__token = None
        self.__refreshToken = None


    def authenticate(self, username, password):
        """
        Authenticate with thingsboard server to obtain JWT token for the user.

        Parameters
        ----------
            username : str
                Username of user for authentication
            password : str
                Password of user for authentication
        """
        url_path = self.url + '/api/auth/login'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        auth_header = {'username': str(username), 'password': str(password)}
        auth_response = requests.post(url=url_path, headers=headers, json=auth_header).json()
        self.__token = auth_response['token']
        self.__refreshToken = auth_response['refreshToken']


    def update_token(self):
        """
        Obtain new token using existing refresh token
        https://github.com/thingsboard/thingsboard/issues/840
        """
        url_path = self.url + '/api/auth/token'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        # The following line may not be needed unsure
        headers["X-Authorization"] = "Bearer " + self.__refreshToken
        auth_header = {'refreshToken': str(self.__refreshToken)}
        auth_response = requests.post(url=url_path, headers=headers, json=auth_header).json()
        self.__token = auth_response['token']
        self.__refreshToken = auth_response['refreshToken']


    def token(self):
        """Returns the main JWT token for the user"""
        return self.__token

    def refreshToken(self):
        """Returns the JWT refreshToken for the user"""
        return self.__refreshToken

    # def token_expired(self):
    #     """Checks if main jwt token is expired"""
    #     try:
    #         jwt.decode(jwt=self.__token, verify=False)
    #     except jwt.ExpiredSignatureError:
    #         return True
    #     else:
    #         return False


class Device(object):
    """
    A class to represent the thingsboard device for Thingsboard REST API.

    ...

    Attributes
    ----------
    account : thingsboard_api.account()
        Account used for device telemetry
    name : str
        Name of device
    device_id : str
        Device ID of the device
    keys : list
        List of keys from thingsboard telemetry

    Methods
    -------
    get_keys():
        Get device keys from thingsboard device telemetry
    get_data(startTs, endTs, keys=None, limit=100000, interval=None, agg=None):
        Get data from thingsboard device telemetry as per REST API
    get_data2(start_time, end_time, keys=None, limit=100000, interval=None, agg=None, tz_offset=10)
        Get data from thingsboard device telemery using datetime interval with timezone offset
    """

    def __init__(self, account, name, device_id):
        """
        Constructs all the necessary attributes for the device object.

        Parameters
        ----------
            account : thingsboard_api.account()
                Account object that contains the url and authentication token
            name : str
                Name of device
            device_id : str
                device id as used by thingsboard
        """
        # assert isinstance(account, Account)
        self.account = account
        self.name = name
        self.device_id = device_id
        self.keys = None


    def get_keys(self):
        """Send a post request to thingsboard telemetry to extract device keys."""
        url_header = self.account.url + \
                '/api/plugins/telemetry/DEVICE/' + str(self.device_id) + \
                '/keys/timeseries'
        headers = {'Content-Type': 'application/json', 'X-Authorization':'bearer '+ str(self.account.token())}
        self.keys = requests.get(url_header, headers=headers).json()
        return self.keys


    def get_data(self, startTs, endTs, keys=None, limit=100000, interval=None, agg=None):
        """
        Sends a post request to thingsboard telemetry to extract device data.
        https://thingsboard.io/docs/user-guide/telemetry/#data-query-api

        Parameters
        ----------
            startTs : int
                Unix timestamp that identifies the start of the interval in milliseconds
            endTs : int
                Unix timestamp that identifies the end of the interval in milliseconds
            keys : list
                List of telemetry keys to fetch
            limit : int
                Max amount of data points to return or intervals to process
            interval : int
                Aggregation interval, in milliseconds
            agg : str
                Aggregation function, one of MIN, MAX, AVG, SUM, COUNT
        
        Returns:
        --------
            Dictionary of telemetry data
        
        Raises:
        -------
            ValueError
        """
        if agg:
            agg = agg.upper()
            if agg.upper() not in ["MIN", "MAX", "AVG", "SUM", "COUNT"]:
                raise ValueError("agg is not one of MIN, MAX, AVG, SUM, COUNT")

        if keys:
            keys_string = ','.join(keys)
        elif self.keys:
            keys_string = ','.join(self.keys)
        else:
            raise ValueError("keys is empty")

        url_header = self.account.url + \
                '/api/plugins/telemetry/DEVICE/' + str(self.device_id) + \
                '/values/timeseries?' + \
                'keys=' + keys_string + \
                '&startTs=' + str(startTs) + \
                '&endTs=' + str(endTs) + \
                '&limit=' + str(limit)
        if interval:
            url_header = url_header + '&interval=' + str(interval)
        if agg:
            url_header = url_header + '&agg=' + str(agg)
        headers = {'Content-Type': 'application/json','X-Authorization': 'bearer '+ str(self.account.token())}
        return requests.get(url_header, headers=headers).json()


    def get_data2(self, start_time, end_time, keys=None, limit=100000, interval=None, agg=None, tz_offset=10):
        """
        Sends a post request to thingsboard telemetry to extract device data from
        datetime interval.
        Uses get_data(self, startTs, endTs, keys=None, limit=100000, interval=None, agg=None)

        Parameters
        ----------
            start_time : datetime.datetime()
                Date and time that identifies the start of the interval
            end_time : datetime.datetime()
                Date and time that identifies the end of the interval
            keys : list
                List of telemetry keys to fetch
            limit : int
                Max amount of data points to return or intervals to process
            interval : int
                Aggregation interval, in milliseconds
            agg : str
                Aggregation function, one of MIN, MAX, AVG, SUM, COUNT
            tz_offset : int
                Timezone hour offset for thingsboard server, defaults for +10 hours
        
        Returns:
        --------
            Dictionary of telemetry data
        
        Raises:
        -------
            ValueError
        """
        assert isinstance(start_time, datetime.datetime)
        assert isinstance(end_time, datetime.datetime)

        # Convert date time to millisecond since unix timestamp for thingsboard
        msecPsec = 1000
        startTs = int((start_time - datetime.datetime(year=1970, month=1, day=1) + \
                datetime.timedelta(hours=tz_offset)).total_seconds() * msecPsec)
        endTs = int((end_time - datetime.datetime(year=1970, month=1, day=1) + \
                datetime.timedelta(hours=tz_offset)).total_seconds() * msecPsec)
        
        return self.get_data(startTs=startTs, endTs=endTs, keys=keys, limit=limit, interval=interval, agg=agg)
    