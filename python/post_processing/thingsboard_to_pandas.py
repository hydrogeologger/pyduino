import sys
import requests
import json
import pandas as pd
import time
import matplotlib.pyplot as plt



class tingsboard_to_pandas:
    def __init__(self,file_path='None',**kwargs ):
        with open(file_path) as data_file:    
            self.input_json = json.load(data_file)
    
    
    
    
    def get_token(self,**kwargs):
        import pdb
        import numpy as np
        import pandas as pd
        #import constants as const
        arg_defaults = {
                    'fn_csv' :'scale_merged.csv',
                    'fn_hd5' :'scale_merged.hd5',
                    'names'  :None,
                    'parse_dates':False,
                    'sep' : '\s+',
                    'header':0,
                    'csv_args':None
                       }
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        url = self.input_json['thingsboard_address']+'/api/auth/login'
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        loginJSON = {'username': self.input_json['username'], 'password': self.input_json['password']}
        tokenAuthResp = requests.post(url, headers=headers, json=loginJSON).json()
        self.input_json['tb_token'] = tokenAuthResp['token']

    
    
    def get_keys(self):
        url = self.input_json['thingsboard_address']+'/api/plugins/telemetry/DEVICE/78144710-a847-11e9-a0ab-e56f74380227/keys/timeseries'
        headers = {'Content-Type': 'application/json','X-Authorization':'bearer '+self.input_json['tb_token']}
        self.input_json["key_list"] = requests.get(url, headers=headers).json()
    
    
    def get_data(self):
        if self.input_json['keys'].lower()=='all':
            self.key_string=','.join(self.input_json['key_list'])
        else:
            self.key_string=self.input_json['keys']
        url= self.input_json['thingsboard_address'] + '/api/plugins/telemetry/DEVICE/'+ self.input_json['device_id']+ '/values/timeseries?keys=' +self.key_string + '&startTs=0&endTs=1563496646595&limit=1000'
        headers = {'Content-Type': 'application/json','X-Authorization':'bearer '+self.input_json['tb_token']}
        self.result_json = requests.get(url, headers=headers).json()

    def convert_data_to_pd(self):
        self.result_pd={   }
        for i in list(self.result_json):
            self.result_pd[i]=pd.DataFrame(self.result_json[i])
            self.result_pd[i]['ts']=pd.to_datetime(self.result_pd[i]['ts'],unit='ms')
            #https://stackoverflow.com/questions/42196337/dataframe-set-index-not-setting/42196399
            self.result_pd[i].set_index('ts',inplace=True,drop=True)


