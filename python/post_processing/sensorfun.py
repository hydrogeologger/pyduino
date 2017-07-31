#http://stackoverflow.com/questions/2682745/how-to-create-a-constant-in-python
import numpy as np
# belwow are all the constants



# permitivity suction fuction
def dielectric_suction_fit(**kwargs):
    '''fit fuction to correlate the suction sensor output to sction value'''
    arg_defaults = {
                'x_offset'  :399.,
                'x_scale'  :5.0,
                'y_scale'  :-20.0,
                'y_offset'  :16.4,
                'lamb':0.65,
                'x':500.
                #'x_offset'  :455.,
                #'x_scale'  :5.0,
                #'y_scale'  :-20.0,
                #'y_offset'  :18.7,
                #'lambda':0.65,
                #'x':500.
                }
    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)
    output=np.zeros(len(np.atleast_1d(arg['x'])))

    for ind,value in enumerate(np.atleast_1d(arg['x'])) :
        if value<arg['x_offset']:
           output[ind]=0
        else:
           output[ind]=np.exp(arg['y_offset']+arg['y_scale'] * (   (value-arg['x_offset'])/arg['x_scale']      )**(-arg['lamb']))
    return output

def dielectric_moisture_fit(**kwargs):
    '''fit fuction to correlate the suction sensor output to sction value'''
    arg_defaults = {
                'x_offset'  :399.,
                'x_scale'  :5.0,
                'y_scale'  :-20.0,
                'y_offset'  :16.4,
                'lamb':0.65,
                'x':500.
                #'x_offset'  :455.,
                #'x_scale'  :5.0,
                #'y_scale'  :-20.0,
                #'y_offset'  :18.7,
                #'lambda':0.65,
                #'x':500.
                }
    arg=arg_defaults
    for d in kwargs:
        arg[d]= kwargs.get(d)
    output=np.zeros(len(np.atleast_1d(arg['x'])))

    for ind,value in enumerate(np.atleast_1d(arg['x'])) :
        if value<arg['x_offset']:
           output[ind]=1.0
        else:
           output[ind]=arg['y_offset']+arg['y_scale'] * (   (value-arg['x_offset'])/arg['x_scale']      )**(-arg['lamb'])
           if output[ind]>1 : output[ind]=1
    return output
