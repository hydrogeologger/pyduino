import sys
import requests
import json
import pandas as pd
import time
import matplotlib.pyplot as plt
import datetime
import constants
import pdb



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
        url = self.input_json['thingsboard_address']+'/api/plugins/telemetry/DEVICE/' + self.input_json['device_id']+  '/keys/timeseries'
        headers = {'Content-Type': 'application/json','X-Authorization':'bearer '+self.input_json['tb_token']}
        self.input_json["key_list"] = requests.get(url, headers=headers).json()
    
    
    def get_data(self):
        if self.input_json['keys'].lower()=='all':
            self.key_string=','.join(self.input_json['key_list'])
        else:
            self.key_string=self.input_json['keys']

        if self.input_json['startTs'].lower()=='':
           self.input_json['startTs_str']='0'
        else:
            date_time = pd.datetime.strptime( self.input_json['startTs']   ,'%Y/%b/%d %H:%M')
            # https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds/35643540
            self.input_json['startTs_str']='%s%03d'%(date_time.strftime("%s"), int(date_time.microsecond/1000))


        if self.input_json['endTs'].lower()=='':
           self.input_json['endTs_str']=str(int(time.time()*constants.msecPsec))
        else:
           date_time = pd.datetime.strptime( self.input_json['endTs']   ,'%Y/%b/%d %H:%M')
           self.input_json['endTs_str']='%s%03d'%(date_time.strftime("%s"), int(date_time.microsecond/1000))

        if self.input_json['limit']=='':
           self.input_json['limit'] = '100000'
           
        #url= self.input_json['thingsboard_address'] + '/api/plugins/telemetry/DEVICE/'+ self.input_json['device_id']+ '/values/timeseries?keys=' +self.key_string + '&startTs=0&endTs=1563496646595&limit=' + self.input_json['limit']
        #pdb.set_trace()
        self.input_json['url_data']= self.input_json['thingsboard_address'] + '/api/plugins/telemetry/DEVICE/'+ self.input_json['device_id']+ '/values/timeseries?keys=' +self.key_string + '&startTs='+ self.input_json['startTs_str'] +  '&endTs='+ self.input_json['endTs_str']+ '&limit=' + self.input_json['limit']
        
        headers = {'Content-Type': 'application/json','X-Authorization':'bearer '+self.input_json['tb_token']}
        self.result_json = requests.get(self.input_json['url_data'], headers=headers).json()

    def convert_data_to_df(self):
        self.result_df={   }
        for i in list(self.result_json):
            #pdb.set_trace()
            print 'converting key '+ i
            self.result_df[i]=pd.DataFrame(self.result_json[i])
            self.result_df[i]['ts']=pd.to_datetime(self.result_df[i]['ts'],unit='ms') +datetime.timedelta(hours=10) # due to UTC time
            #https://stackoverflow.com/questions/42196337/dataframe-set-index-not-setting/42196399
            self.result_df[i].set_index('ts',inplace=True,drop=True)
            self.result_df[i].sort_index(inplace=True)
            #self.result_df[i].to_numeric('value',inplace=True)
            #df['b'] = pd.to_numeric(df['b'], errors='coerce'
            self.result_df[i]['value']=pd.to_numeric(self.result_df[i]['value'],errors='coerce')

     


    def plot_df(self,plot_input):
        fig = plt.figure(figsize=(16,10))
        ax = [[] for i in range(30)]
        ax[0  ] = plt.subplot2grid((1, 1), (0, 0), colspan=1)
        #ax[1  ] = plt.subplot2grid((3, 1), (1, 0), colspan=1)
        for i in plot_input:
            print i
            ax[0].plot(self.result_df[i]['value'])
        #im1 = ax[0 ].plt(scale_1_df.index,scale_1_df['value'])
        #ax[0]=plt.plot(scale_1_df.index,scale_1_df['value'])
        #ax[0].plot(scale_1_df['value'])
        #ax[1].plot(scale_2_df['value'])
        plt.show(block=False)
