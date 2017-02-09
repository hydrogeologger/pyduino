#http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
import numpy as np
# belwow are all the constants
g2kg = 0.001
kg2g = 1000.
ms2mmday=3600.*24*1000
kelvin=273.15
mm2m=0.001
m2mm=1000.
rhow_pure_water=1000
g=9.8
second2day=1./3600/24
kg2g=1000.
g2kg=0.001
psych=62.2  # pa/K  # https://en.wikipedia.org/wiki/Psychrometric_constant

#class constitutive_relation:

def dv(tk):
    ''' using temperature to calculate water vapor diffusivity (m2/s)
     y = dv(tk) 
     tk -- temperature in kelvin'''
    return 2.29e-5*(tk/273.15)**1.75
   
def rhovs(tk):
     ''' def y = rhovs(tk)
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
   

#    g2kg = 0.001
#    kg2g = 1000.
#    ms2mmday=3600.*24*1000
#    kelvin=273.15
#    mm2m=0.001
#    m2mm=1000.
#    rhow_pure_water=1000
#    g=9.8
#    second2day=1./3600/24
#    kg2g=1000.
#    g2kg=0.001
#    #self.psim_log_range=-[0.0001:0.0001:0.001,0.002:0.001:0.01,0.02:0.01:0.1,0.2:0.1:1,2:1:10,20:10:100,200:100:1000,2000:1000:10000,20000:10000:1e5...
#    #	,2e5:1e5:1e6,2e6:1e6:9e6,1e7:1e7:9e7,1e8:1e8:9e8]
#    mol_weight_water=0.018 #kg/mol
#    R =8.314
#    def __init__(self):
#        self.g2kg = 0.001
#        self.kg2g = 1000.
#        self.ms2mmday=3600.*24*1000
#        self.kelvin=273.15
#        self.mm2m=0.001
#        self.m2mm=1000.
#        self.rhow_pure_water=1000
#        self.g=9.8
#        self.second2day=1./3600/24
#        self.kg2g=1000.
#        self.g2kg=0.001
#        #self.psim_log_range=-[0.0001:0.0001:0.001,0.002:0.001:0.01,0.02:0.01:0.1,0.2:0.1:1,2:1:10,20:10:100,200:100:1000,2000:1000:10000,20000:10000:1e5...
#        #	,2e5:1e5:1e6,2e6:1e6:9e6,1e7:1e7:9e7,1e8:1e8:9e8]
#        self.mol_weight_water=0.018 #kg/mol
#        self.R =8.314
#    def area(self):
#        return self.x * self.y
#    def perimeter(self):
#        return 2 * self.x + 2 * self.y
#    def describe(self,text):
#        self.description = text
#    def authorName(self,text):
#        self.author = text
#    def scaleSize(self,scale):
#        self.x = self.x * scale
#        self.y = self.y * scale
