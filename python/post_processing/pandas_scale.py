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


        self.parse_dates=arg['parse_dates']

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
                #self.df_sub[i]=pd.read_csv(fn,**kwargs ) #,names=arg['names'],parse_dates=arg['parse_dates'],header=arg['header'])

                #self.df_sub[i]=pd.read_csv(fn,sep=arg['sep'],names=arg['names'],parse_dates=arg['parse_dates'],
                #    header=arg['header'],date_parser=arg['date_parser'])
                self.df_sub[i]=pd.read_csv(fn,sep=arg['sep'],names=arg['names'], header=arg['header'],date_parser=arg['date_parser'],parse_dates=arg['parse_dates'],index_col=arg['index_col'])
                #print i,','
                #self.df_sub[i]=pd.read_csv(fn,sep=arg['sep'],names=['sensor1','sensor2','sensor3','sensor4','sensor5','sensor6'], header=arg['header'],date_parser=arg['date_parser'])

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
                self.df=pd.concat(self.df_sub,axis=0).sort_values(self.parse_dates)
                # http://stackoverflow.com/questions/16167829/in-pandas-how-can-i-reset-index-without-adding-a-new-column
                # to make sure that it re list the system
                self.df=self.df.reset_index(drop=True)
                print i,','
            elif i==1:
                self.df=self.df_sub[0]
            else:
                print 'no file has been extracted, please ensure the directory is ended with slash! '

            
             
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
        self.df=self.df.sort_values(self.parse_dates).reset_index(drop=True)
        

            
             
        
            
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
        
        


    
class concat_data_tb():
#"""
#this is to creat new data series that are ready to be interpolated
#"""
    import pandas as pd
    #def __init__(self,start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
    #def __init__(self,start_time=inp_start_time,end_time=inp_end_time,dt_s=inp_dt_s):
    def __init__(self,start_time,end_time,dt_s):
    #def __init__(self): #start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
	import pdb
        import csv
	import numpy as np
        import pandas as pd
        self.dt_s=dt_s
        #pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),period=pd.Timedelta(600,unit='s' ) )
        # frequency is actually the duration between the neighbouring point not period
        #date_time=pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),freq=pd.Timedelta(600,unit='s' ) )

        #pdb.set_trace()
        date_time=pd.date_range(start=start_time,end=end_time,freq=pd.Timedelta(dt_s,unit='s' ) )
        self.df = pd.DataFrame({ 'date_time' : date_time})
        self.df['time_days']=(self.df['date_time']-self.df['date_time'][0]).astype('timedelta64[s]')/86400.0
        self.df.set_index('date_time',inplace=True,drop=True)
    

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

    def merge_data_from_tb(self,**kwargs ):
        '''
        import matplotlib.pyplot as plt
        #    properties:
        #      rm_nan --  whether delete the nan data
        #      keys   --  the property that needs to be interpolated
        #      df     --  the panel data that gets the source data
         
        the var_in needs to be in the format like [pd['time'],['scale1', 'scale2']  ] '''
        import pdb
        import pandas as pd
        import polynomial
        import interpolate as wf
        #import wafo.interpolate as wf

        # below is optional
        arg_defaults = {'plot':    False,
                    'keys': ['scale'],
                    'newkeys':None ,
                    'coef': 1e-14,
                    'rm_nan':True,
                    'key_name':None,
                    'mask':None,
                    'time_index':'date_time',
                    'input_time_series':None,
                    'input_data_series':None,
                    'output_time_series':None,
        }
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        
        #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        input_time_ay_s=((arg['input_time_series']-arg['input_time_series'][0])/np.timedelta64(1,'s')).values

        # TO181023 making sure that we can name a new string
        # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
        if arg['rm_nan']==True:
            mask_idx          =  arg['input_data_series'].isnull()
            input_time_ay_no_nan =  input_time_ay_s[~mask_idx]
            input_data_ay_no_nan  =  arg['input_data_series'][~mask_idx]
            interp_method     =  wf.SmoothSpline(input_time_ay_no_nan,input_data_ay_no_nan,p=arg['coef'])
        else:
            interp_method=wf.SmoothSpline(input_time_ay_s,arg['input_data_series'],p=arg['coef'])
        # warning, it is found that the Smoothspline is dependent on the x axis!!!
        output_time_ay_sec=((arg['output_time_series'] - arg['input_time_series'][0]  )/np.timedelta64(1,'s')).values

        self.df[arg['key_name']]=interp_method(output_time_ay_sec)
        #pdb.set_trace()
        #if arg['mask'] == None:
        #    self.df[arg['key_name']]=interp_method(output_time_ay_sec)
        #else:
        #    self.df[arg['key_name']][arg['mask']]=interp_method(output_time_ay_sec)
        
        if arg['plot']==True:
            import matplotlib.pyplot as plt 
            fig = plt.figure() 
            fig.subplots_adjust(bottom=0.2)
            fig.canvas.set_window_title('interpolate ')
            plt.plot(arg['input_time_series'], arg['input_data_series']  ,'b+', markersize=15)
            plt.plot(arg['output_time_series'],self.df[  arg['key_name']  ],'ro')
            plt.title('interpolated '+arg['key_name']+' result, coef='+str(arg['coef']))
            plt.xticks(rotation=45)
            plt.show(block=False)


class concat_data_roof():
#"""
#this is to creat new data series that are ready to be interpolated
#"""
    import pandas as pd
    #def __init__(self,start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
    #def __init__(self,start_time=inp_start_time,end_time=inp_end_time,dt_s=inp_dt_s):
    def __init__(self,start_time,end_time,dt_s):
    #def __init__(self): #start_time=pd.Timestamp('2016-06-25 08:46:30'),end_time=pd.Timestamp('2016-07-11 01:00:56'),dt_s=600):
	import pdb
        import csv
	import numpy as np
        import pandas as pd
        self.dt_s=dt_s
        #pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),period=pd.Timedelta(600,unit='s' ) )
        # frequency is actually the duration between the neighbouring point not period
        #date_time=pd.date_range(start=pd.Timestamp('2016-06-25 08:46:30'),end=pd.Timestamp('2016-07-11 01:00:56'),freq=pd.Timedelta(600,unit='s' ) )

        #pdb.set_trace()
        date_time=pd.date_range(start=start_time,end=end_time,freq=pd.Timedelta(dt_s,unit='s' ) )
        self.df = pd.DataFrame({ 'date_time' : date_time})
        self.df['time_days']=(self.df['date_time']-self.df['date_time'][0]).astype('timedelta64[s]')/86400.0


    
    
#    def merge_data(self,var_in=a ): this is not good because if a is not defined, this is not going to be useful
    def merge_data(self,**kwargs ):
        '''
        import matplotlib.pyplot as plt
        #    properties:
        #      rm_nan --  whether delete the nan data
        #      keys   --  the property that needs to be interpolated
        #      df     --  the panel data that gets the source data
        in case the error is TypeError: descriptor '__sub__' requires a 'datetime.datetime' object but received a 'float'
        the problem could be that the datetime axis has NaN or NaT inside. TO200501
        the var_in needs to be in the format like [pd['time'],['scale1', 'scale2']  ] 
        '''
        import pdb
        import pandas as pd
        import polynomial
        import interpolate as wf
        #import wafo.interpolate as wf

        # below is optional
        arg_defaults = {'plot' : False,
                    'keys'     : ['scale'],
                    'newkeys'  : None ,
                    'coef'     : 1e-14,
                    'rm_nan'   : True,
                    'new_keys' : None,
                    'mask'     : None}
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        # below is essential
        source_df=arg['df']
        source_keys=arg['keys']

        #if arg['plot']==True:
        #    pdb.set_trace()
        # check if source_df has NaT TO200501
        nat_bool=np.isnat(source_df.index)
        total_number_of_nat=np.sum(nat_bool)
        location_nat=np.where(nat_bool)
        if total_number_of_nat!=0:
            print(str(total_number_of_nat)+ 'of  NaT exists in the time array as merge source df='
                    +'row number'+str(location_nat[0][0]) + 'to'+ str(location_nat[0][-1]) +'\n'   )
                    #+source_df.index.loc[location_nat])
            return

        nat_bool=np.isnat(self.df.index)
        total_number_of_nat=np.sum(nat_bool)
        location_nat=np.where(nat_bool)
        if total_number_of_nat!=0:
            print(str(total_number_of_nat)+ 'of  NaT exists in the base time array'
                    +'row number'+str(location_nat[0][0]) + 'to' + str(location_nat[0][-1]) +'\n'   )
                    #+source_df.index.loc[location_nat])
            return
        
        if arg['new_keys']==None:
            arg['new_keys']=source_keys
        #else:
        #    for i in arg['new_keys']:
        #        arg['new_keys'][i]=arg['keys'][i]
        
        #pdb.set_trace()
        #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        source_df.drop_duplicates(subset='date_time', keep='first',inplace=True)
        source_sec=(source_df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
        #pdb.set_trace()

        # TO181023 making sure that we can name a new string
        # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
        for idx,i in enumerate(source_keys):
            if arg['rm_nan']==True:
                
                #pdb.set_trace()
                mask_idx          =  source_df[ i   ].isnull()
                source_sec_no_nan =  source_sec[~mask_idx]
                source_df_no_nan  =  source_df[ i   ][~mask_idx]
                interp_method     =  wf.SmoothSpline(source_sec_no_nan,source_df_no_nan,p=arg['coef'])
            else:
                interp_method=wf.SmoothSpline(source_sec,source_df[ i   ],p=arg['coef'])
            #interp_method=wf.SmoothSpline(source_sec,source_df[ i   ],p=arg['coef'])
            # warning, it is found that the Smoothspline is dependent on the x axis!!!
            sp_sec=(self.df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
            #self.df[i]=interp_method(sp_sec)
            if arg['mask'] == None:
                self.df[ arg['new_keys'][idx] ]=interp_method(sp_sec)
            else:
                self.df[ arg['new_keys'][idx] ][arg['mask']]=interp_method(sp_sec)
        
            if arg['plot']==True:
                #fig, ax = plt.subplots(2,sharex=False)
                import matplotlib.pyplot as plt 
                fig = plt.figure() 
                fig.subplots_adjust(bottom=0.2)
                fig.canvas.set_window_title('interpolate '+ i)
                plt.plot(source_df['date_time'],source_df [i]  ,'b+')
                plt.plot(self.df['date_time'],self.df[  arg['new_keys'][idx]  ],'ro')
                plt.title('interpolated '+i+' result, coef='+str(arg['coef']))
                plt.xticks(rotation=45)
                plt.show(block=False)
            # http://stackoverflow.com/questions/28694025/converting-a-datetime-column-back-to-a-string-columns-pandas-python
            #cc=b.df['date_time'].dt.strftime('%Y-%m-%d')
        #  http://stackoverflow.com/questions/17134716/convert-dataframe-column-type-from-string-to-datetime
        #bbb=pd.to_datetime( b.df['date_time'])

         #(g[9]-g[1])/np.timedelta64(1, 's')
         #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        #(self.df['date_time']-self.df['date_time'][0])/np.timedelta64(1, 's') 




#    def merge_data2(self,var_in=a ): this is not good because if a is not defined, this is not going to be useful
    def merge_data2(self,**kwargs ):
        '''
        subroutine to slice data
        the difference between merge_data2 and merge data is merge data2 uses all the data for interpolation
        merge_data_only use choped results
        import matplotlib.pyplot as plt
        #    properties:
        #      rm_nan --  whether delete the nan data
        #      keys   --  the property that needs to be interpolated
        #      df     --  the panel data that gets the source data
        # start_time  --  the start time that slice works example starttime=np.datetime64('2018-04-11T10:00')
        #   end_time  --  the start time that slice works example starttime=np.datetime64('2018-04-11T10:00')
        in case the error is TypeError: descriptor '__sub__' requires a 'datetime.datetime' object but received a 'float'
        the problem could be that the datetime axis has NaN or NaT inside. TO200501
        particularly be aware of NaT because null can not filter this out.
         
        the var_in needs to be in the format like [pd['time'],['scale1', 'scale2']  ] 
        '''
        import pdb
        import pandas as pd
        #import wafo.interpolate as wf
        import polynomial
        import interpolate as wf

        arg_defaults = {'plot'   : False,
                    'keys'       : ['scale'],
                    'newkeys'    : None ,
                    'coef'       : 1e-14,
                    'rm_nan'     : True,
                    'start_time' : None,
                    'end_time'   : None}
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        #this is composory
        source_df=arg['df']  # this is the whole panel
        #this is composory
        source_keys=arg['keys']  # the keys needs to be interpolated
        if arg['start_time']==None: arg['start_time']= self.df['date_time'][0]
        if arg['end_time']  ==None: arg['end_time']= self.df['date_time'].iloc[-1]
          
        #for i in arg['new_keys']:
        #    if i==None : arg['new_keys'][i]=
        
        #pdb.set_trace()
        #http://stackoverflow.com/questions/14920903/time-difference-in-seconds-from-numpy-timedelta64
        #source_sec=(source_df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
        #mask_source_df=source_df0['date_time'].between(arg['start_time'],arg['end_time'])
        #mask_source_df=
        #source_df=source_df0[mask_source_df]
        source_df=arg['df']




        #if arg['plot']==True:
        #    pdb.set_trace()
        # check if source_df has NaT TO200501
        nat_bool=np.isnat(source_df.index)
        total_number_of_nat=np.sum(nat_bool)
        location_nat=np.where(nat_bool)
        if total_number_of_nat!=0:
            print(str(total_number_of_nat)+ 'of  NaT exists in the time array as merge source df='
                    +'row number'+str(location_nat[0][0]) + 'to'+ str(location_nat[0][-1]) +'\n'   )
                    #+source_df.index.loc[location_nat])
            return

        nat_bool=np.isnat(self.df.index)
        total_number_of_nat=np.sum(nat_bool)
        location_nat=np.where(nat_bool)
        if total_number_of_nat!=0:
            print(str(total_number_of_nat)+ 'of  NaT exists in the base time array'
                    +'row number'+str(location_nat[0][0]) + 'to' + str(location_nat[0][-1]) +'\n'   )
                    #+source_df.index.loc[location_nat])
            return



        #pdb.set_trace()
        # this is not going to work for slicing as the first row is not indexed as 0
        #source_sec=(source_df['date_time']-source_df['date_time'][0])/np.timedelta64(1,'s')
        #source_sec=(source_df['date_time']-source_df['date_time'].iloc[0])/np.timedelta64(1,'s')

        # the two below is exactly the same thing
        source_sec=(arg['df']['date_time']-datetime.datetime(1970,1,1)).dt.total_seconds()
        # this one is found not working for mac 
        #source_sec=(arg['df']['date_time']-np.datetime64('1970-01-01')).dt.total_seconds()
        for i in source_keys:
            if arg['rm_nan']==True:
                
                #pdb.set_trace()
                mask_idx          =  source_df[ i   ].isnull()
                source_sec_no_nan =  source_sec[~mask_idx]
                source_df_no_nan  =  source_df[ i   ][~mask_idx]
                interp_method     =  wf.SmoothSpline(source_sec_no_nan,source_df_no_nan,p=arg['coef'])
            else:
                interp_method=wf.SmoothSpline(source_sec,source_df[ i   ],p=arg['coef'])
            #interp_method=wf.SmoothSpline(source_sec,source_df[ i   ],p=arg['coef'])
            # warning, it is found that the Smoothspline is dependent on the x axis!!!
            mask_slice=self.df['date_time'].between(arg['start_time'],arg['end_time'])
            sp_sec=(self.df[mask_slice]['date_time']-datetime.datetime(1970,1,1)).dt.total_seconds()
            
            #sp_sec=(self.df['date_time']-source_df['date_time'].iloc[0])/np.timedelta64(1,'s')

            #sp_sec=(source_df['date_time']-source_df['date_time'].iloc[0])/np.timedelta64(1,'s')

            #sp_sec=(arg['start_time']-arg['end_time'][0])/np.timedelta64(1,'s')
            #mask_new_array=self.df['date_time'].between(arg['start_time'],arg['end_time'])
            # TO180413 the below is not going to assign values to pandas
            #self.df[mask_new_array][i] = interp_method(sp_sec)
            #pdb.set_trace()
            #self.df.loc[mask_new_array,i] = interp_method(sp_sec)
            #self.df.iloc[i] = interp_method(sp_sec)
            self.df.loc[mask_slice,i] = interp_method(sp_sec)
            
            #self.df[i].between(arg['start_time'],arg['end_time']) = interp_method(sp_sec)
        
            if arg['plot']==True:
                #fig, ax = plt.subplots(2,sharex=False)
                import matplotlib.pyplot as plt 
                fig = plt.figure() 
                fig.subplots_adjust(bottom=0.2)
                fig.canvas.set_window_title('interpolate '+ i)
                plt.plot(source_df['date_time'],source_df [i]  ,'b+')
                plt.plot(self.df[mask_slice]['date_time'],self.df[mask_slice][i],'ro')
                plt.title('interpolated '+i+' result, coef='+str(arg['coef']))
                plt.xticks(rotation=45)
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
