#An example of a class
# http://sthurlow.com/python/lesson08/
# anything puts in here 
import numpy as np
import constants as const
import datetime
class scale:
    # this is the comments for scale 
    def __init__(self,fn):
	import pdb
        import csv
	import numpy as np
        import constants as const
        ## below part is working
        ## http://stackoverflow.com/questions/3925614/how-do-you-read-a-file-into-a-list-in-python
        #with open('site_address.csv') as f:
        #    self.lines = f.read().splitlines()

        #http://stackoverflow.com/questions/24662571/python-import-csv-to-list
        #self.lines = []
        #with open('site_address.csv', 'r') as f:
        #    for line in f.readlines():
        #        l,name = line.strip().split(',')
        #        self.lines.append((l,name))

        #http://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list-with-python
        # TO 20160516 it seems to me that it is better of to deal with csv completely and then do others based on the list created in this loop
        print 'Initializing class scale  ...'
        with open(fn, 'rb') as f:
            # this below doesn't work well with your_list
            #self.station_no = sum(1 for row in f)
            reader    = csv.reader(f)
            your_list = list(reader)
            #self.x=reader.split(',')
            #[self.strip() for self in reader.split(',')]

        self.data_no  = len(your_list)-1
        self.date_str = ["" for x in range(self.data_no)]
        self.time_str = ["" for x in range(self.data_no)]
        self.time_dt  = ["" for x in range(self.data_no)]
        #np.zeros(self.data_no,dtype=float)
        #self.time_str=np.zeros(self.data_no,dtype=float)
        self.scale1   = np.zeros(self.data_no,dtype=float)
        self.stable1  = np.zeros(self.data_no,dtype=bool)
        ## method 1, it ends up with list that each cell is a list
        ## http://stackoverflow.com/questions/3880037/how-to-create-a-list-or-tuple-of-empty-lists-in-python
        #self.station_name=[list(someListOfElements) for _ in xrange(self.station_no)]

        # method 2, it ends up with list that each cell is a string
        # http://stackoverflow.com/questions/6376886/what-is-the-best-way-to-create-a-string-array-in-python
        #self.station_name = ["" for x in range(self.data_no)]        

	#pdb.set_trace()
        for n in np.arange(self.data_no):
            tmp=your_list[n][0].split()
            self.date_str[n]=tmp[0]
            self.time_str[n]=tmp[1]
	    self.time_dt[n]= datetime.datetime.strptime(
		self.date_str[n]+' '+self.time_str[n]
		,'%d/%b/%Y %H:%M:%S')
            self.scale1[n]  =float(tmp[2])*const.g2kg
	    if len(tmp)==4:
                if tmp[3]=='g':
	            self.stable1[n]=True
	    else:
	        self.stable1[n]=False


        #print 'file',fn,'has %d data points, starting from ',
	#self.time_dt[0].strftime('%d/%b/%Y %H:%M:%S'), ' to ',
        #self.time_dt[-1].strftime('%d/%b/%Y %H:%M:%S') %(self.data_no)
        #aa=self.time_dt[0].strftime('%d %b %Y %H %M %S')
        #bb=self.time_dt[0].strftime('%d %b %Y %H %M %S')
        #print 'file',fn,'has %d data points, starting from ' %(self.data_no)
	print '    file',fn,'has %d data points,' %(self.data_no)
        print '    starting from',  self.time_dt[0],'to', self.time_dt[-1] 


    def append_file(self,fn):
	import pdb
	import csv
	import numpy as np
	import datetime
        import constants as const
        with open(fn,'rb') as f:
	    self.reader=csv.reader(f)
	    your_list=list(self.reader)
        self.data_no_ap=len(your_list)-1        
        #date_str_ap = ["" for x in range(self.data_no_ap)]
        #time_str_ap = ["" for x in range(self.data_no_ap)]
        self.time_dt_ap  = ["" for x in range(self.data_no_ap)]
        self.scale1_ap   = np.zeros(self.data_no_ap,dtype=float)
        self.stable1_ap  = np.zeros(self.data_no_ap,dtype=bool)
        self.tmp= ["" for x in range(self.data_no_ap)]

        
	for n in np.arange(self.data_no_ap):
	    #pdb.set_trace()
            tmp=your_list[n][0].split()
            #self.date_str_ap[n]=tmp[0]
            #self.time_str_ap[n]=tmp[1]
	    self.time_dt_ap[n]= datetime.datetime.strptime(
		tmp[0]+' '+tmp[1]
		,'%d/%b/%Y %H:%M:%S')
            self.scale1_ap[n]  =float(tmp[2])*const.g2kg
	    if len(tmp)==4:
                #pdb.set_trace()
                if tmp[3]=='g':
	            self.stable1_ap[n]=True
	    else:
	        self.stable1_ap[n]=False
	    
        print 'Appending file',fn, 'has %d data points,' %(self.data_no_ap)
        print '    from',  self.time_dt_ap[0],'to', self.time_dt_ap[-1] 

        if self.time_dt_ap[0]>self.time_dt[-1]:  # all data can be appended to end
	    self.time_dt = np.append( self.time_dt , self.time_dt_ap)
	    self.scale1     = np.append( self.scale1  , self.scale1_ap)
	    self.stable1    = np.append( self.stable1  , self.stable1_ap)
            data_no_prev=self.data_no
            self.data_no+=self.data_no_ap
            print '    Putting new data to the end of the database'
        elif self.time_dt_ap[-1]<self.time_dt[0]:
	    self.time_dt = np.append( self.time_dt_ap , self.time_dt)
	    self.scale1  = np.append( self.scale1_ap  , self.scale1)
	    self.stable1  = np.append( self.stable1_ap  , self.stable1)
            data_no_prev=self.data_no
            self.data_no+=self.data_no_ap
            print '    Putting new data to the beginning of the database'
        else:
            print '    Putting file to the middle of the database'    
            for n in np.arange(self.data_no):
		if self.time_dt_ap[0]>self.time_dt[n] and self.time_dt_ap[-1] < self.time_dt[n+1]: 
                    print '    Inserting between',  self.time_dt[n],'and', self.time_dt[n+1],'in database' 
	            print '    At line %d' %(n)
	            self.time_dt = np.append(np.append(self.time_dt[:n] , self.time_dt_ap ), self.time_dt[n:])
	            self.scale1  = np.append(np.append(self.scale1 [:n] , self.scale1_ap  ), self.scale1[n:] )
	            self.stable1  = np.append(np.append(self.stable1 [:n] , self.stable1_ap  ), self.stable1[n:] )
                    data_no_prev = self.data_no
                    self.data_no+=self.data_no_ap
		    break
                if n==self.data_no-1:
                    print '    this file has been added before'
                    data_no_prev=self.data_no
                    self.data_no_ap=0

        print '    now database has %d + %d = %d data points' %(data_no_prev,self.data_no_ap,self.data_no)
        print '    starting from',  self.time_dt[0],'to', self.time_dt[-1] 

    def plot_scale_readings(self):
        ''' plot_scale_readings from scale1
                some things to it '''
        # let me write something
        import matplotlib.pyplot as plt
        import datetime
        import matplotlib.dates as mdates
        #http://stackoverflow.com/questions/15261260/plot-date-and-time-x-axis-versus-a-value-y-axis-using-data-from-file
        #fig=plt.figure(figsize=(20,15))
        fig, ax = plt.subplots()
        ax.plot_date(self.time_dt,self.scale1,'r+')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%b')) 
        ax.grid(True)
        #plt.plot( np.arange(self.data_no),self.scale1,'r+')
        #plt.plot( datetime.datetime.strftime(self.time_dt, '%d/%b'),self.scale1,'r+')
        #plt.plot( datetime.datetime.strftime(str(self.time_dt), '%d/%b'),self.scale1,'r+')
        #plt.plot( self.time_dt,self.scale1,'r+')
        plt.ylabel('SCALE WEIGHT (kg)')
        plt.xlabel('TIME')
        fname='scale_readings.png'
        fig.savefig(fname,format='png')
        plt.savefig(fname)
        return fig.show()

    def spline_scale_readings(self,**kwargs):
        import wafo.interpolate as wf
        import matplotlib.pyplot as plt
        import datetime
        import matplotlib.dates as mdates
        import numpy as np
        import pdb
        
        arg_defaults = {'coef':    0.01,
            'time_interval_sec_sp': 0}
        arg=arg_defaults
        for d in kwargs:
            arg[d]= kwargs.get(d)

        self.time_sec=np.array([datetime.timedelta.total_seconds(self.time_dt[i]-self.time_dt[0]) for i in range(len(self.time_dt))])
        if arg['time_interval_sec_sp'] <>0:
            self.time_sec_sp=np.arange(self.time_sec[0],self.time_sec[-1],arg['time_interval_sec_sp'])
            self.time_dt_sp = [self.time_dt[0]+datetime.timedelta(seconds=n) for n in self.time_sec_sp]
        else:
            self.time_sec_sp=self.time_sec
            self.time_dt_sp=self.time_dt
        
        # two set
        interp_method=wf.SmoothSpline(self.time_sec,self.scale1,p=arg['coef'])
        self.scale1_sp=interp_method(self.time_sec_sp)


        # script to calculate the derivatives of the scale
        self.evap_rate=-np.append(np.diff(self.scale1_sp),np.nan)/self.surf_area1/arg['time_interval_sec_sp']/const.rhow_pure_water

        fig, ax = plt.subplots(2,sharex=True)
        ax[0].plot_date(self.time_dt,self.scale1,'r+')
        ax[0].plot_date(self.time_dt_sp,self.scale1_sp,'go')
        ax[0].xaxis.set_major_formatter(mdates.DateFormatter('%d/%b')) 
        ax[0].grid(True)
        ax[0].set_ylabel('SCALE WEIGHT (kg)')
        plt.xlabel('TIME')
        fig.suptitle(['coef= ' + str(arg['coef'])+' time_interval_sec_sp= '+ str(arg['time_interval_sec_sp'])], fontsize=20)

        #ax[1].plot_date(self.time_dt,self.scale1,'r+')
        ax[1].plot_date(self.time_dt_sp,self.evap_rate*const.ms2mmday,'go')
        ax[1].grid(True)
        ax[1].set_ylabel('EVAP. (mm/day)')




        fname='spline_coef'+str(arg['coef'])+'.png'
        fig.savefig(fname,format='png')
        return fig.show()




    def export_data_as_csv(self,fn):
         import numpy as np
         f = open(fn, 'w',0)
         for n in np.arange(self.data_no-1):
             if self.stable1[n] == True :
                 sw_stable=', 1'
             else:
                 sw_stable=', 0'
             f.write(self.time_dt[n].strftime("%d/%b/%Y %H:%M:%S")+'  ,  '+str(self.scale1[n])+sw_stable+'\n')
         f.close()

#############################################################################
        

    def interpolate_values_as_mtx(self,lats,lons):
        from scipy.interpolate import griddata
        from scipy.interpolate import Rbf
        self.lats_mtx=lats
        self.lons_mtx=lons
        self.interp_evap_annual_mmday_mtx    = [np.zeros(lats.shape,dtype=float) for _ in np.arange(day_count_yearly.size)]
        self.interp_rain_annual_mmday_mtx    = [np.zeros(lats.shape,dtype=float) for _ in np.arange(day_count_yearly.size)]
        self.interp_net_evap_annual_mmday_mtx= [np.zeros(lats.shape,dtype=float) for _ in np.arange(day_count_yearly.size)]

        for n in np.arange(self.days_annual.size):
            # transpose a 1-D np array is not trivial
            # http://stackoverflow.com/questions/19238024/transpose-of-a-vector-using-numpy
            # data format for gridata
            #  http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.interpolate.griddata.html
            #  gridata(x and y(1000,2),value(1000),[500 500],method=cubic)
            # several takes in gridata
            # 1. it doesn't extrapolate
            # 2. cubic tends to over estimate
            # 3. linear is good but not very accurate
            # 4. nearest is the most uggly one
            self.interp_evap_annual_mmday_mtx[n] = griddata(np.hstack([self.latitude[np.newaxis, :].T,self.longitude[np.newaxis, :].T]), self.evap_annual_mmday[n], (self.lats_mtx, self.lons_mtx), method='linear')
            self.interp_rain_annual_mmday_mtx[n] = griddata(np.hstack([self.latitude[np.newaxis, :].T,self.longitude[np.newaxis, :].T]), self.rain_annual_mmday[n], (self.lats_mtx, self.lons_mtx), method='linear')
            self.interp_net_evap_annual_mmday_mtx[n] = self.interp_evap_annual_mmday_mtx[n] -self.interp_rain_annual_mmday_mtx[n] 

            ## now we are using rbf TO  2015-05-17
            ##https://scipy.github.io/old-wiki/pages/Cookbook/RadialBasisFunctions.html
            ## seems it is a bit slow
            ## a better way of improving evaporation interploation is to interpolate the final net evap data
            #aa=Rbf(self.latitude,self.longitude,self.evap_annual_mmday[n], epsilon=2)
            #self.interp_evap_annual_mmday_mtx[n] = aa(self.lats_mtx, self.lons_mtx)
            #bb=Rbf(self.latitude,self.longitude,self.rain_annual_mmday[n], epsilon=2)
            #self.interp_rain_annual_mmday_mtx[n] = bb(self.lats_mtx, self.lons_mtx)




        # it is funny that python doesn't have a function to average a list
        # http://stackoverflow.com/questions/9039961/finding-the-average-of-a-list
        self.interp_evap_total_avg_mmday_mtx = sum(self.interp_evap_annual_mmday_mtx)/float(len(self.interp_evap_annual_mmday_mtx))
        self.interp_rain_total_avg_mmday_mtx = sum(self.interp_rain_annual_mmday_mtx)/float(len(self.interp_rain_annual_mmday_mtx))
        self.interp_net_evap_total_avg_mmday_mtx=self.interp_evap_total_avg_mmday_mtx-self.interp_rain_total_avg_mmday_mtx


        # the below result only do one interpolation based on the averaged last image
        self.one_interp_evap_total_avg_mmday_mtx = griddata(np.hstack([self.latitude[np.newaxis, :].T,self.longitude[np.newaxis, :].T]), self.evap_total_avg_mmday, (self.lats_mtx, self.lons_mtx), method='linear')
        self.one_interp_rain_total_avg_mmday_mtx = griddata(np.hstack([self.latitude[np.newaxis, :].T,self.longitude[np.newaxis, :].T]), self.rain_total_avg_mmday, (self.lats_mtx, self.lons_mtx), method='linear')
        self.one_interp_net_evap_total_avg_mmday_mtx=griddata(np.hstack([self.latitude[np.newaxis, :].T,self.longitude[np.newaxis, :].T]), self.evap_total_avg_mmday-self.rain_total_avg_mmday, (self.lats_mtx, self.lons_mtx), method='linear')




        
    def plot_interpolated_annual_avg_result(self):
        for n in np.arange(len(self.days_annual)):
            fig=plt.figure(figsize=(20,25))
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            ax3 = fig.add_subplot(313)
            #v = np.linspace(-0.02,0.02, 21, endpoint=True)
            
            im=ax1.contourf(self.lons_mtx,self.lats_mtx,self.interp_evap_annual_mmday_mtx[n]) #,levels=v)
            ax1.plot(self.longitude,self.latitude,'r+')
            ax1.set_ylabel('latitude')
            ax1.set_title('Interpolated average Evaporation (mm/day) in '+str(1979+n))
            fig.colorbar(im,ax=ax1) #,ticks=v)
            #print 'the max evap is: '+str(np.max(evap_total))+'m, minimum evap is: '+ str(np.min(evap_total))+' m'
            #
            #
            im=ax2.contourf(self.lons_mtx,self.lats_mtx,self.interp_rain_annual_mmday_mtx[n]) #,levels=v)
            ax2.plot(self.longitude,self.latitude,'r+')
            ax2.set_ylabel('latitude')
            ax2.set_title('Interpolated average Precipitation (mm/day) in '+str(1979+n))
            fig.colorbar(im,ax=ax2)
            #print 'the max rain is: '+str(np.max(rain_total))+'m, minimum evap is: '+ str(np.min(rain_total))+' m'
            #
            ##print 'Processing time'+ unicode(data_date_rain)+ ', for precipitation finished'+str(lats.shape)
            #
            im=ax3.contourf(self.lons_mtx,self.lats_mtx,self.interp_net_evap_annual_mmday_mtx[n]) #,levels=v)
            ax3.plot(self.longitude,self.latitude,'r+')
            ax3.set_title('Interploated average Evaporation-precipitation (mm/day) in ' +str(1979+n))
            ax3.set_ylabel('latitude')
            ax3.set_xlabel('longitude')
            #ax3.set_title('Precipitation + evaporation (m) at UTC time: '
            #    +unicode(data_date)+ ' or Beijing time:'
            #    +unicode(data_date+datetime.timedelta(hours=+8) ))
            fig.colorbar(im,ax=ax3)
            #fig.show()
            #
            print 'interpolated_average_evaporatoin_rain_in_year_'+ str(1979+n)+'.png'
            fig_name='interpolated_average_evaporatoin_rain_in_year_'+ str(1979+n)+'.png'
            csv_name_rain='interpolated_annual_average_evaporation_mmday_in_year_'+str(1979+n)+'.csv'
            csv_name_evap='interpolated_annual_average_rain_mmday_in_year_'+str(1979+n)+'.csv'
            csv_name_total='interpolated_annual_average_net_evaporation_mmday_in_year_'+str(1979+n)+'.csv'
            
            #np.savetxt(csv_name_rain, evap_annual_avg_mmday, delimiter=",")
            #np.savetxt(csv_name_evap, rain_annual_avg_mmday, delimiter=",")
            #np.savetxt(csv_name_total, evap_annual_avg_mmday-rain_annual_avg_mmday, delimiter=",")
            fig.savefig(fig_name,format='png')
            plt.close(fig)
        
    def plot_interpolated_total_avg_result(self):
            fig=plt.figure(figsize=(20,25))
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            ax3 = fig.add_subplot(313)
            #v = np.linspace(-0.02,0.02, 21, endpoint=True)
        
            
            im=ax1.contourf(self.lons_mtx,self.lats_mtx,self.interp_evap_total_avg_mmday_mtx) #,levels=v)
            ax1.plot(self.longitude,self.latitude,'r+')
            ax1.set_ylabel('latitude')
            ax1.set_title('Interpolated average Evaporation (mm/day) over 32 years' )
            fig.colorbar(im,ax=ax1) #,ticks=v)
            #print 'the max evap is: '+str(np.max(evap_total))+'m, minimum evap is: '+ str(np.min(evap_total))+' m'
            #
            #
            im=ax2.contourf(self.lons_mtx,self.lats_mtx,self.interp_rain_total_avg_mmday_mtx) #,levels=v)
            ax2.plot(self.longitude,self.latitude,'r+')
            ax2.set_ylabel('latitude')
            ax2.set_title('Interpolated average Precipitation (mm/day) over 32 years')
            fig.colorbar(im,ax=ax2)
            #print 'the max rain is: '+str(np.max(rain_total))+'m, minimum evap is: '+ str(np.min(rain_total))+' m'
            #
            ##print 'Processing time'+ unicode(data_date_rain)+ ', for precipitation finished'+str(lats.shape)
            im=ax3.contourf(self.lons_mtx,self.lats_mtx,
                self.interp_evap_total_avg_mmday_mtx-self.interp_rain_total_avg_mmday_mtx)
            ax3.plot(self.longitude,self.latitude,'r+')
            ax3.set_title('Interploated average Evaporation-precipitation (mm/day) over 32 years')
            ax3.set_ylabel('latitude')
            ax3.set_xlabel('longitude')
            #ax3.set_title('Precipitation + evaporation (m) at UTC time: '
            #    +unicode(data_date)+ ' or Beijing time:'
            #    +unicode(data_date+datetime.timedelta(hours=+8) ))
            fig.colorbar(im,ax=ax3)
            #fig.show()
            #
            print 'interpolated_total_avg_evap_rain.png'
            #csv_name_total='interpolated_annual_average_net_evaporation_mmday_in_year_'+str(1979+n)+'.csv'
            #np.savetxt(csv_name_rain, evap_annual_avg_mmday, delimiter=",")
            #np.savetxt(csv_name_evap, rain_annual_avg_mmday, delimiter=",")
            #np.savetxt(csv_name_total, evap_annual_avg_mmday-rain_annual_avg_mmday, delimiter=",")
            fig_name='interpolated_average_evap_rain_in_total.png'
            fig.savefig(fig_name,format='png')
            plt.close(fig)



            # the below is the image that only does the one off image
            fig=plt.figure(figsize=(20,25))
            ax1 = fig.add_subplot(311)
            ax2 = fig.add_subplot(312)
            ax3 = fig.add_subplot(313)
            #v = np.linspace(-0.02,0.02, 21, endpoint=True)
            
            im=ax1.contourf(self.lons_mtx,self.lats_mtx,self.one_interp_evap_total_avg_mmday_mtx) #,levels=v)
            ax1.plot(self.longitude,self.latitude,'r+')
            ax1.set_ylabel('latitude')
            ax1.set_title('Interpolated average Evaporation (mm/day) over 32 years' )
            fig.colorbar(im,ax=ax1) #,ticks=v)
            #print 'the max evap is: '+str(np.max(evap_total))+'m, minimum evap is: '+ str(np.min(evap_total))+' m'
            #
            #
            im=ax2.contourf(self.lons_mtx,self.lats_mtx,self.one_interp_rain_total_avg_mmday_mtx) #,levels=v)
            ax2.plot(self.longitude,self.latitude,'r+')
            ax2.set_ylabel('latitude')
            ax2.set_title('Interpolated average Precipitation (mm/day) over 32 years')
            fig.colorbar(im,ax=ax2)
            im=ax3.contourf(self.lons_mtx,self.lats_mtx,
                self.one_interp_evap_total_avg_mmday_mtx-self.one_interp_rain_total_avg_mmday_mtx)
            ax3.plot(self.longitude,self.latitude,'r+')
            ax3.set_title('Interploated average Evaporation-precipitation (mm/day) over 32 years')
            ax3.set_ylabel('latitude')
            ax3.set_xlabel('longitude')
            fig.colorbar(im,ax=ax3)
            #fig.show()
            #
            print 'one_interpolated_total_avg_evap_rain.png'
            csv_name_total_evap='one_interpolated_total_avg_evap_mmday_over_32_years.csv'
            csv_name_total_rain='one_interpolated_total_avg_rain_mmday_over_32_years.csv'
            csv_name_total_net_evap='one_interpolated_total_avg_net_evap_mmday_over_32_years.csv'
            np.savetxt(csv_name_total_evap, self.one_interp_evap_total_avg_mmday_mtx, delimiter=",")
            np.savetxt(csv_name_total_rain, self.one_interp_rain_total_avg_mmday_mtx, delimiter=",")
            np.savetxt(csv_name_total_net_evap, self.one_interp_evap_total_avg_mmday_mtx-self.one_interp_rain_total_avg_mmday_mtx, delimiter=",")
            fig_name='one_interpolated_average_evap_rain_in_total.png'
            fig.savefig(fig_name,format='png')
            plt.close(fig)
        
    def area(self):
        return self.x * self.y
    def perimeter(self):
        return 2 * self.x + 2 * self.y
    def describe(self,text):
        self.description = text
    def authorName(self,text):
        self.author = text
    def scaleSize(self,scale):
        self.x = self.x * scale
        self.y = self.y * scale
    #  print a.fn_no_stations()
    def fn_no_stations(self):
        return self.row_count


    def output_csv_for_station(self):
        #http://stackoverflow.com/questions/2721521/fastest-way-to-generate-delimited-string-from-1d-numpy-array
        year_str=np.char.mod('%i', np.arange(1979,2011))
        year_str_comma_sep = ",".join(year_str)
        header='station_name,'+year_str_comma_sep+',total_average'
        
        # http://stackoverflow.com/questions/14134237/writing-data-from-a-python-list-to-csv-row-wise
        #writer=csv.writer(open('aaa.csv','wb',0))
        #header=['type','id','numberOfUpdates','isPingEnabled','lastUpdated']
        #length_list=len(header)
        #for word in header:
        #    writer.writerow([word])
        fid= open('evap_per_station.csv','wb',0)
        fid.write(header)
        fid.write('\n')
        for n in np.arange(a.station_no):
            line=np.char.mod('%e', np.append( np.array([self.evap_annual_mmday[i][n] for i in np.arange(len( self.evap_annual_mmday))]) , self.evap_total_avg_mmday[n]))
            line= ",".join(line)
            line=self.station_name[n]+','+line
            fid.write(line)
            fid.write('\n')
        fid.close()



        fid= open('rain_per_station.csv','wb',0)
        fid.write(header)
        fid.write('\n')
        for n in np.arange(a.station_no):
            line=np.char.mod('%e', np.append( np.array([self.rain_annual_mmday[i][n] for i in np.arange(len( self.rain_annual_mmday))]) , self.rain_total_avg_mmday[n]))
            line= ",".join(line)
            line=self.station_name[n]+','+line
            fid.write(line)
            fid.write('\n')
        fid.close()
    
        fid= open('net_evap_per_station.csv','wb',0)
        fid.write(header)
        fid.write('\n')
        for n in np.arange(a.station_no):
            line=np.char.mod('%e', np.append( np.array([self.net_evap_annual_mmday[i][n] for i in np.arange(len( self.net_evap_annual_mmday))]) , self.net_evap_total_avg_mmday[n]))
            line= ",".join(line)
            line=self.station_name[n]+','+line
            fid.write(line)
            fid.write('\n')
        fid.close()
#import csv
#with open('site_address.csv', 'rb') as f:
#    reader = csv.reader(f)
#    your_list = list(reader)
#
#print your_list
