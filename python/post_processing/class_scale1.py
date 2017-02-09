#An example of a class
# http://sthurlow.com/python/lesson08/
class Station:
    def __init__(self,fname):
        import csv
        import numpy as np
        #with open('site_address.csv', 'rb') as csvfile:
        #with open('site_address.csv', 'rb') as csvfile:
        #    fn = csv.reader(csvfile, delimiter=',')
        #    # to save the file in to the class, one needs to define as self.row_count
        #    self.station_no = sum(1 for row in fn)
        #    self.station_name=[list() for _ in xrange(self.station_no)]
        #    n=0
        #    #for row in fn:
        #    for row in fn:
        #        self.content = list(row[i] for i in fn)
        #    #     self.station_name[n] = row
        #    #     n+=1
        #        print ', '.join(row)
        #    #self.n=n


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
        with open('site_address.csv', 'rb') as f:
            # this below doesn't work well with your_list
            #self.station_no = sum(1 for row in f)
            reader = csv.reader(f)
            your_list = list(reader)
            #self.x=reader.split(',')
            #[self.strip() for self in reader.split(',')]

        self.station_no=len(your_list)
        self.latitude=np.zeros(self.station_no,dtype=float)
        self.longitude=np.zeros(self.station_no,dtype=float)
        ## method 1, it ends up with list that each cell is a list
        ## http://stackoverflow.com/questions/3880037/how-to-create-a-list-or-tuple-of-empty-lists-in-python
        #self.station_name=[list(someListOfElements) for _ in xrange(self.station_no)]

        # method 2, it ends up with list that each cell is a string
        # http://stackoverflow.com/questions/6376886/what-is-the-best-way-to-create-a-string-array-in-python
        self.station_name = ["" for x in range(self.station_no)]        

        for n in np.arange(self.station_no):
            self.station_name[n]=your_list[n][0]
            self.latitude[n]=float(your_list[n][1])
            self.longitude[n]=float(your_list[n][2])

    description = "This shape has not been described yet"
    author = "Nobody has claimed to make this shape yet"

    def plot_stations(self):
        import matplotlib.pyplot as plt
        fig=plt.figure(figsize=(20,15))
        plt.plot(self.longitude,self.latitude,'r+')
        plt.ylabel('latitude')
        plt.xlabel('longitude')
        fig.savefig('station_location.png',format='png')
        #return fig.show()


    def find_lats_lons_idx_from_mtx(self,lats,lons):
        import operator
        lats_ay=lats[:,1]
        lons_ay=lons[1,:]
        self.lats_idx=np.zeros(self.station_no,dtype=int)
        self.lons_idx=np.zeros(self.station_no,dtype=int)
        for n in np.arange(self.station_no):
            #http://stackoverflow.com/questions/2474015/getting-the-index-of-the-returned-max-or-min-item-using-max-min-on-a-list
            self.lats_idx[n], min_value = min(enumerate(abs(a.latitude[n] -lats_ay)), key=operator.itemgetter(1))
            self.lons_idx[n], max_value = min(enumerate(abs(a.longitude[n]-lons_ay)), key=operator.itemgetter(1))

    def extract_value_at_stations(self,evap_yearly_raw,rain_yearly_raw,lats,lons,day_count_yearly
        ,evap_total_rate_mmday,rain_total_rate_mmday):
        # define a list of empty np array:
        #result = [np.zeros(5) for _ in xrange(3)]
        # result = [np.random.rand(5) for _ in xrange(3)]
        # get the first column
        # b=[result[n][0] for n in xrange(2)]   # this ends up with a list
        # c=c=np.array([result[n][0] for n in xrange(2)])   # this ends up with a np array
        self.evap_annual_mmday    = [np.zeros(self.station_no,dtype=float) for _ in np.arange(day_count_yearly.size)]   
        self.rain_annual_mmday    = [np.zeros(self.station_no,dtype=float) for _ in np.arange(day_count_yearly.size)]   
        self.net_evap_annual_mmday= [np.zeros(self.station_no,dtype=float) for _ in np.arange(day_count_yearly.size)]   
        self.evap_total_avg_mmday       = np.zeros(self.station_no,dtype=float)
        self.rain_total_avg_mmday       = np.zeros(self.station_no,dtype=float)
        self.net_evap_total_avg_mmday   = np.zeros(self.station_no,dtype=float)
        #self.days_annual          = np.zeros(days_count_yearly.size,dtype=float)
        self.days_annual=day_count_yearly

        for n in np.arange(day_count_yearly.size):
           # although we plot evap and rain by plot(lons,lats,evap), the evap and rain is stored by evap[lats, lons, steps]
           self.evap_annual_mmday[n]     = -evap_yearly_raw[self.lats_idx,self.lons_idx,n]*1000/day_count_yearly[n]
           self.rain_annual_mmday[n]     = rain_yearly_raw[self.lats_idx,self.lons_idx,n]*1000/day_count_yearly[n]
           self.net_evap_annual_mmday[n] = self.evap_annual_mmday[n]-self.rain_annual_mmday[n]

        self.evap_total_avg_mmday     = evap_total_rate_mmday[self.lats_idx,self.lons_idx]
        self.rain_total_avg_mmday     = rain_total_rate_mmday[self.lats_idx,self.lons_idx]
        self.net_evap_total_avg_mmday =  self.evap_total_avg_mmday-self.rain_total_avg_mmday 
        

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
