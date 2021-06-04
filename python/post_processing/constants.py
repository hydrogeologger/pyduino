#http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
import numpy as np
# belwow are all the constants
g2kg = 0.001
kg2g = 1000.
ms2mmday=3600.*24*1000
mmdayPms=1.0/3600/24/1000
msPmmday=3600*24*1000

dayPs = 1/(60*60*24)
sPday =60*60*24
kelvin=273.15
mm2m=0.001
m2mm=1000.
rhow_pure_water=1000
g=9.8
second2day=1./3600/24
kg2g=1000.
g2kg=0.001
psych=62.2  # pa/K  # https://en.wikipedia.org/wiki/Psychrometric_constant
molecular_weight_water=0.018
R=8.314
air_density_kgPm3=1.27
heat_capacity_air_JPkgPK=1010.0
kgPg=0.001
gPkg=1000.
mmPm=1000.
mPmm=.001
gPkg = 1000.
kgPg = 0.001
msPmmday=3600.*24*1000
psychrometric_paPK=66.0
mPkm=1000
kmPm=0.001
minutePday=60.*24
secPmsec=1e-3 # convert milli second to second
msecPsec=1000 # convert second to milli second
#class constitutive_relation:

def dv(tk):
    ''' using temperature to calculate water vapor diffusivity (m2/s)
     y = dv(tk) 
     tk -- temperature in kelvin'''
    return 2.29e-5*(tk/273.15)**1.75
   
def rhovs(tk):
     ''' def y = rhovs(tk)
      Saturated vapour density
      (S)aturated water (V)apor density (rho) at EM(5)0 channel (C) [rhovs]
      tk -- temperature in kelvin'''
     return  1e-3*np.exp(19.819-4976/tk)

def drhovs(tk):
    ''' the derivative of (S)aturated (V)apor density
    input temperature in kelvin'''
    return 4.976/tk**2.*np.exp(19.819-4976/tk)


def rht(psi,tk):
    '''(R)elative (H)umidi(T)y
    rht(psi,tk)'''
    return np.exp(-psi*9.81*0.018/8.314/tk)

    
def  svp(tk):
    '''(S)aturated water (V)apor (P)ressure 
    def  svp(t)
    input temperature in kelvin
    output saturated vapor pressure in pascal'''
    return  611.0*np.exp(17.27*(tk-273.15)/(tk-35.85))

def  dsvp_dtk(tk):
    '''the derivative of (S)aturated water (V)apor (P)ressure with respect to Temperature 
    input temperature in kelvin
    '''
    return  4098./(tk-35.85)**2*svp(tk)

def lhv(tk):
    '''(L)atent (H)eat for (V)aporization
    def lhv(t) 
    The input is temperature in kelvin
    The output unit is Joule/kg'''
    return 2500250.-2365.*(tk-273.15)


def rs1994(sw,por):
    '''(S)urface (R)esistance from (V)an (D)er (G)riv 1994 Griend
    def rs1994(sw,por)'''
    return 10.*np.exp(35.63*(0.15-sw*por))


def rs1986(sw,por):
    '''(S)urface (R)esistance from Camillo et al. [1986]
    def rs1986(sw,por)'''
    return -805.+4140.*por*(1-sw)


def rs1996(sw,por):
    '''(S)urface (R)esistance from Daamen et al. [1996]'''
    return 3.e10*(por*(1-sw))**16.6

def rs1984(sw):
    '''(S)urface (R)esistance from Sun et al. [1984]'''
    return 3.5*(sw)**(-2.3)+33.5
   
def swcc_fredlund_xing_1994(**kwargs):
    '''Soil water retention curve from Fredlund and Xing [1994]
    input explanation:
    af -- [kPa] a soil parameter which is primarily a function of air entry value
    nf -- a soil parameter which is primarily a function of the rate of water extraction from the soil once the air-entry value has been exceeded
    mf -- a soil parameter which is primarily a function of the residual water content
    hr -- [kPa] suction at which residual water contents occurrs 
    por-- porosity
    psi-- input suction range [kPa]
    '''
    psi_default=np.arange(10**-4,10**-4,10**-4)
    for i in np.arange(-3,6):
       new=np.arange(10.0**float(i),10.**(float(i)+1.),10.**float(i))
       psi_default=np.concatenate((psi_default,new))
    arg_defaults = {
                'plot':True,
                'nf'  :0.85,
                'mf'  :0.31,
                'af'  :24.9999,
                'hr'  :223873.8,
                'por':0.54,
                'psi':psi_default}
    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)
    
    #tmp1=(arg['psi']/arg['a'])**arg['n']
    #tmp2=np.log(np.e+tmp1)
    #tmp3=arg['por']*(1./tmp2)**arg['m']



    tmp1=1  -  np.log(1+arg['psi']/arg['hr'])  /  np.log(1+1.0e6/arg['hr'])
    tmp2=np.exp(1)+(arg['psi']/arg['af'])**arg['nf']
    tmp3=np.log(tmp2)**arg['mf']
    tmp4=arg['por']*tmp1*(1/tmp3)
    if arg['plot']:
        import matplotlib.pyplot as plt
        import matplotlib.pylab as pylab


        params = {'legend.fontsize': 13,
                  'figure.figsize': (10, 5),
                 'axes.labelsize': 12,
                 'axes.titlesize':'x-large',
                 'xtick.labelsize':'20',
                 'ytick.labelsize':'20',
        #         'ytick.labelweight':'bold',
                  'axes.labelsize': 16,
                   'axes.labelweight':'bold'}
        #         'axes.grid':'linewidth=grid_width,color = '0.5''}
        #         'linewidth':lw,'markers.size':ms,'markers.edgewidth':mew}
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams["axes.labelweight"] = "bold"
        pylab.rcParams.update(params)
        
        
        
        fig = plt.figure(figsize=(12,12))
        
        fig.subplots_adjust(left=0.18, right=0.98, top=0.99, bottom=0.15)
        lw=4
        ms=12
        mew=4
        grid_width=2
        y_fontsize=25
        
        
        ax = fig.add_subplot(111)
        for axis in ['top','bottom','left','right']:
          ax.spines[axis].set_linewidth(2) 
        
        #sp_sch[sch_name].te_fit=np.polyfit(sp_sch[sch_name].df['commercial'],sp_sch[sch_name].df['te'],1)
        #legend_string_second_te="%.3e" % sp_sch[sch_name].te_fit[0] + ' * x +' "%.3e" % sp_sch[sch_name].te_fit[1]
        #legend_string_first_te="%.3e" % sp_sch[sch_name].te_fit[0] + ' * x +' "%.3e" % sp_sch[sch_name].te_fit[1]

        plt.semilogx(arg['psi'],tmp4 ,'ro',linewidth=lw,label='SWCC')
        plt.grid(linewidth=grid_width,color = '0.5')

        plt.xlabel('SOIL SUCTION (kPa)', fontsize=y_fontsize, labelpad=15)
        plt.ylabel('GRAVIMETRIC WATER CONTENT (g)', fontsize=y_fontsize, labelpad=15)

    return tmp4, arg['psi']


def swcc_reverse_fredlund_xing_1994(**kwargs):
    '''Soil water retention curve from Fredlund and Xing [1994]
      reversing calculating from content to suction
      input should be volumetric water content
      output unit is kpa
      input:
      input explanation:
      af -- [kpa] a soil parameter which is primarily a function of air entry value
      nf -- a soil parameter which is primarily a function of the rate of water extraction from the soil once the air-entry value has been exceeded
      mf -- a soil parameter which is primarily a function of the residual water content
      hr -- [kpa] suction at which residual water contents occurrs 
      por-- porosity
      psi_0  -- the suction kpa when volumetric water content is saturated
      '''
    arg_defaults = {
                'nf'  :0.85,
                'mf'  :0.31,
                'af'  :24.9999,
                'hr'  :223873.8,
                'por':0.54,
                'vwc':0.1,
                'psi_0':1e-1,
                'psi_1':0.02  
                }

    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)

    psi_outcome=np.zeros(len(np.atleast_1d(arg['vwc'])))

    for i,k in enumerate(np.atleast_1d(arg['vwc'])) :
        #import pdb
#        psi_1=0.02  # after a testing, the starting point would be good to be near the saturation level
        psi_1=arg['psi_1'] #2020-01-03 
#        psi_1=arg['af']  #2017-07-08 16:27 turns out the air entry pressure is the best start guessing point 
        psi_0=arg['psi_0'] #2020-01-03
        
        #pdb.set_trace()
        if k>=arg['por']:
            psi_1=arg['psi_0']
        else:
            while abs(psi_0-psi_1)>0.0001:
                psi_0=psi_1

                psi_on_af  = psi_0/arg['af']
                log_on_log =  np.log(1+psi_0/arg['hr']) / np.log(1+1.e6/arg['hr']) 

                e_plus    = np.e+psi_on_af**arg['nf']
                log_e      = np.log(e_plus) 
                dw_dpsi_0   =  - arg['mf']*arg['nf']*psi_on_af**(-1+arg['nf']) * arg['por'] * (1- log_on_log) * log_e **(-1-arg['mf']) /  arg['af'] / e_plus - arg['por']* log_e**(-arg['mf'])/arg['hr']/(1+psi_0/arg['hr'])/np.log(1+1.e6/arg['hr'])


                tmp1=1  -  np.log(1+psi_0/arg['hr'])  /  np.log(1+1.0e6/arg['hr'])
                tmp2=np.exp(1)+(psi_0/arg['af'])**arg['nf']
                tmp3=np.log(tmp2)**arg['mf']
                w_0=arg['por']*tmp1*(1/tmp3)-k


                psi_1= psi_0 - w_0/dw_dpsi_0
        #print psi_1
        psi_outcome[i] = psi_1


    return psi_outcome

def latlon_two_ponts_to_delta_xy_m(latlon1, latlon2):
    '''
    def latlon_two_ponts_to_delta_xy([lat1,lon1] [lat2,lon2]):
    https://stackoverflow.com/questions/24617013/convert-latitude-and-longitude-to-x-and-y-grid-system-using-python
    input 
    out put in meters
    latlon1 is the origin point
    '''
    #dx = (lon2-lon1)*40000*np.cos((lat1+lat2)*np.pi/360)/360
    #dy = (lat1-lat2)*40000/360
    dx = (latlon2[1]-latlon1[1])*40000*np.cos((latlon1[0]+latlon2[0])*np.pi/360)/360*mPkm
    dy = (latlon2[0]-latlon1[0])*40000/360*mPkm
    return [dx,dy]
