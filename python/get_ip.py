import socket
import fcntl
import struct
import numpy as np

def get_ip_address_string(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

#get_ip_address('eth0')  # '192.168.0.110'
def get_ip_address_string_error_tolerant(ifname):
    try:
        return get_ip_address_string(ifname)
    except:
        return []


def get_ip_address_digit(ifname):
    ip_string=get_ip_address_string_error_tolerant(ifname)
    if ip_string!=[]:
        x=np.array(ip_string.split('.'), dtype='|S4')
        return  x.astype(np.int)
    else:
        return  np.array([0,0,0,0], dtype='int')

        
def get_ip_address_digit_mask(ifname):
    ip_digit=get_ip_address_digit(ifname)
    return ip_digit[3]*10000+ip_digit[2]
    #if len(ip_digit)==4:
    #    return  ip_digit[2]*1000+ip_digit[3]
    #else:
    #    return  
    
