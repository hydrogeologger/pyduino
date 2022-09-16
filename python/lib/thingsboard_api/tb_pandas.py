#!/usr/bin/env python
"""
Module provides pandas wrapper function to support thingsboard_api.

Dependencies:
-------------
    thingsboard_api : REST API for thingsboard
    pandas : For data post processing
"""
import datetime
import pandas as pd
# import matplotlib.pyplot as plt
from .__init__ import Device as tb_device

# from python.lib import thingsboard_api
class Device(tb_device):
    """
    A class to represent the thingsboard device for Pandas. Child class of
    thingsboard_api.Device

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
    data : dict/json
        Data as requested from device telemetry

    Methods
    -------
    In addition of thingsboard_api.Device() methods
    get_dataframe():
        Returns the device time series telemetry in pandas.dataframe format.
    """
    def __init__(self, *args, **kwargs):
        super(Device, self).__init__(*args, **kwargs)
        self.data = None


    def get_data(self, *args, **kwargs):
        """
        Overrides thingsboard_api.Device.get_data() to store telemetry data in object
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
        self.data = super(Device, self).get_data(*args, **kwargs)
        return self.data


    def get_data2(self, *args, **kwargs):
        """
        Overrides thingsboard_api.Device.get_data2() to store telemetry data in object
        Sends a post request to thingsboard telemetry to extract device data.
        https://thingsboard.io/docs/user-guide/telemetry/#data-query-api

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
        self.data = super(Device, self).get_data2(*args, **kwargs)
        return self.data


    def get_dataframe(self, keys=None, tz_offset=10):
        """
        Construct a Pandas.DataFrame object from device timeseries telemetry

        Parameters
        ----------
            keys : list
                List of telemetry keys to limit for data frame
            tz_offset : int
                Timezone hour offset for thingsboard server, defaults for +10 hours
        
        Returns:
        --------
            Dictionary of data in Pandas.DataFrame format
        """
        result_df = {}
        if keys is None:
            keys = self.data

        for key in keys:
            #pdb.set_trace()
            print('converting key ' + key)
            result_df[key] = pd.DataFrame(self.data[key])
            result_df[key]['ts'] = pd.to_datetime(result_df[key]['ts'], unit='ms') + datetime.timedelta(hours=tz_offset)  # due to UTC time
            #https://stackoverflow.com/questions/42196337/dataframe-set-index-not-setting/42196399
            result_df[key].set_index('ts', inplace=True, drop=True)
            result_df[key].sort_index(inplace=True)
            #result_df[key].to_numeric('value',inplace=True)
            #df['b'] = pd.to_numeric(df['b'], errors='coerce'
            result_df[key]['value'] = pd.to_numeric(result_df[key]['value'], errors='coerce')
        return result_df
