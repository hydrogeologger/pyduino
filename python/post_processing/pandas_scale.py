# ~/Dropbox/tailing_column/data/column_on_roof
# df=pd.read_csv('/home/chenming/Dropbox/tailing_column/data/column_on_roof/scale_2016_Jul_01.dat')
#df=pd.read_csv(fn,sep='     | ',engine='python')
#names=['foo', 'bar', 'baz']
#df=pd.read_csv(fn,sep='     | ',engine='python',names=['foo', 'bar', 'baz'])
#
#
#df=pd.read_csv(fn,sep='      | ',engine='python')
#[8599 rows x 4 columns]
import os
import sys
import numpy as np
#import constants as const
import datetime
class pandas_scale:
    #def __init__(self,file_path,source='raw',fn_csv='scale_merged.csv',fn_hd5='scale_merged.hd5'):
    # http://stackoverflow.com/questions/9867562/pass-kwargs-argument-to-another-function-with-kwargs
    # this is the best way of sorting variables. file_path and sources are
    # variables used for the current init function, while others will be 
    # consumed by subfunctions
    def __init__(self,file_path='None',source='raw',**kwargs ):

	import pdb
        import csv
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


        #fn='/home/chenming/Dropbox/tailing_column/data/column_on_roof/'
        sys.path.append(file_path)
        # no good as it does not exclude other non-directory
        #self.file_list_scale_roof=os.listdir(file_path)
        
        
        #from os.path import isfile, join
        #from os import listdir
        # below gives the files with the entire list
        import glob
        self.file_path_list=glob.glob(file_path+"*.dat")

        #with open(file_list_column_roof,'rb') as f:
        #    self.reader=csv.reader(f)
        #    your_list=list(self.reader)
        self.raw_file_path=file_path
        self.concat_file_path=file_path+'merged_data/'
        #pdb.set_trace()
        
        if source=='raw':  # merging the data from raw files
            self.no_files=len(self.file_path_list)
            self.df_sub=[[] for _ in xrange(len(self.file_path_list))]
            i=0
            for fn in self.file_path_list:
                print 'Parsing '+fn+', %d/%d' %(i,len(self.file_path_list))
                # through multiple trial and error
                # http://stackoverflow.com/questions/38561268/parsing-data-using-pandas-with-fixed-sequence-of-strings/38561323#38561323
                #pdb.set_trace()
                #self.df_sub[i]=pd.read_csv(fn,sep=arg['sep'],names=arg['names'],parse_dates=arg['parse_dates'],header=arg['header'])
                self.df_sub[i]=pd.read_csv(fn,**kwargs ) #,names=arg['names'],parse_dates=arg['parse_dates'],header=arg['header'])
                # http://stackoverflow.com/questions/10972410/pandas-combine-two-columns-in-a-dataframe
                #self.df[i]['a']= self.df[i]['a'].map(str)+' '+self.df[i]['b']
                ##http://stackoverflow.com/questions/13411544/delete-column-from-pandas-dataframe 
                #self.df[i].__delitem__('b')
                ##http://stackoverflow.com/questions/17134716/convert-dataframe-column-type-from-string-to-datetime
                ##convert string to datetime
                #self.df[i]['a'] = pd.to_datetime(self.df[i]['a'])
                i+=1
            #http://pandas.pydata.org/pandas-docs/stable/merging.html
            # sorting the results using 
            #pdb.set_trace()
            if i>1: 
                self.df=pd.concat(self.df_sub,axis=0).sort(['date_time'])
                # http://stackoverflow.com/questions/16167829/in-pandas-how-can-i-reset-index-without-adding-a-new-column
                # to make sure that it re list the system
                self.df=self.df.reset_index(drop=True)
            else:
                self.df=self.df_sub[0]

            
             
        elif source=='csv':
            print 'Parsing '+self.concat_file_path+arg['fn_csv']
            self.df=pd.read_csv(self.concat_file_path+arg['fn_csv'],sep='\s+',names=['date','time','scale','stable'],parse_dates=[['date','time']])
        elif source=='hdf5':
            print 'Parsing '+self.concat_file_path+arg['fn_hd5']
            store = pd.HDFStore(self.concat_file_path+arg['fn_hd5'])
            self.df=store['df']



    def append_file(self,file_path=None,**kwargs ):
	import pdb
        import csv
	import numpy as np
        import pandas as pd
        #arg_defaults = {
        #            'fn_hd5' :'scale_merged.hd5',
        #            'names'  :None,
        #            'parse_dates':False,
        #            'sep' : '\s+',
        #            'header':0,
        #            'csv_args':None
        #               }
        #arg=arg_defaults
        #for d in kwargs:
        #    arg[d]= kwargs.get(d)


        sys.path.append(file_path)
        import glob
        self.append_file_path_list=glob.glob(file_path+"*.dat")
        #pdb.set_trace()

        self.append_file_list=os.listdir(file_path)
        self.no_files=len(self.append_file_path_list)
        self.df_sub=[[] for _ in xrange(len(self.append_file_path_list))]
        i=0
        for fn in self.append_file_path_list:
            print 'Parsing appending'+fn+', %d/%d' %(i,len(self.file_path_list))
            self.df_sub[i]=pd.read_csv(fn,**kwargs ) #,names=arg['names'],parse_dates=arg['parse_dates'],header=arg['header'])
            self.df=pd.concat([self.df,self.df_sub[i]])
            i+=1
        self.df=self.df.sort(['date_time']).reset_index(drop=True)
        

            
             
        
            
    def save_as_csv(self,fn='scale_merged.csv'):
        import os
        folder_merged_data_exist=os.path.isdir(self.concat_file_path)
        if not folder_merged_data_exist: os.mkdir(self.concat_file_path)
        print 'Saving dataframe to ' + self.concat_file_path+fn

        self.df.to_csv(self.concat_file_path+fn, sep='\t', encoding='utf-8',date_format="%d/%b/%Y %H:%M:%S"
               ,index=False,header=False)

    def save_as_hdf5(self,fn='scale_merged.hd5'):
        import pandas as pd
        folder_merged_data_exist=os.path.isdir(self.concat_file_path)
        if not folder_merged_data_exist: os.mkdir(self.concat_file_path)
        print 'Saving dataframe as hdf5 file...'+ self.concat_file_path+fn
        # http://stackoverflow.com/questions/17098654/how-to-store-data-frame-using-pandas-python 
        store = pd.HDFStore(self.concat_file_path+fn)
        store['df'] = self.df
        
        


    
class concat_data_roof:
    import pandas as pd
    def __init__(self,start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
    #def __init__(self): #start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
	import pdb
        import csv
	import numpy as np
        import pandas as pd
        self.dt_s=600
        #pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),period=pd.Timedelta(600,unit='s' ) )
        # frequency is actually the duration between the neighbouring point not period
        #date_time=pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),freq=pd.Timedelta(600,unit='s' ) )
        date_time=pd.date_range(start=start_time,end=end_time,freq=pd.Timedelta(dt_s,unit='s' ) )
        self.df = pd.DataFrame({ 'date_time' : date_time})
        self.df['time_days']=(self.df['date_time']-self.df['date_time'][0]).astype('timedelta64[s]')/86400.0




    
    
#    def merge_data(self,var_in=a ): this is not good because if a is not defined, this is not going to be useful
    def merge_data(self,**kwargs ):
        import pdb
        import pandas as pd
        import wafo.interpolate as wf
        import matplotlib.pyplot as plt
        "the var_in needs to be in the format like [pd['time'],['scale1', 'scale2']  ]"
        arg_defaults = {'plot':    False,
                    'keys': ['scale'],
                    'newkeys':None ,
                    'coef': 1e-14}
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        source_df=arg['df']
        source_keys=arg['keys']
        #for i in arg['new_keys']:
        #    if i==None : arg['new_keys'][i]=
        
        #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        source_sec=(source_df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
        #pdb.set_trace()

        for i in source_keys:
            interp_method=wf.SmoothSpline(source_sec,source_df[ i   ],p=arg['coef'])
            # warning, it is found that the Smoothspline is dependent on the x axis!!!
            sp_sec=(self.df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
            self.df[i]=interp_method(sp_sec)
        
        
        
            if arg['plot']==True:
                fig, ax = plt.subplots(2,sharex=False)
                ax[0].plot(source_df['date_time'],source_df [i]  ,'b+')
                ax[0].plot(self.df['date_time'],self.df[i],'ro')
                ax[0].set_title('interpolated '+i+' result')
                plt.show(block=False)
            # http://stackoverflow.com/questions/28694025/converting-a-datetime-column-back-to-a-string-columns-pandas-python
            #cc=b.df['date_time'].dt.strftime('%Y-%m-%d')
        #  http://stackoverflow.com/questions/17134716/convert-dataframe-column-type-from-string-to-datetime
        #bbb=pd.to_datetime( b.df['date_time'])

         #(g[9]-g[1])/np.timedelta64(1, 's')
         #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        #(self.df['date_time']-self.df['date_time'][0])/np.timedelta64(1, 's') 
    def get_derivative(self,**kwargs ):
        import pandas as pd
        import matplotlib.pyplot as plt
        #var_in= [a.df,['scale']]  
        arg_defaults = {'plot':    False,
                    'key': ['cum_evap'],
                    'deri_key':['evap']
                       }
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)
        self.df[arg['deri_key']]=np.append(np.diff(self.df[arg['key']] ),np.nan)/self.dt_s

