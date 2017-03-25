import numpy as np
import cv2
from pylepton import Lepton
from collections import Iterable
import csv
import time
import os
time_now=time.strftime("%Y_%b_%d_%H_%M_%S")


os.chdir('/home/pi/pypleton/')

file_name= 'flir.csv'
fid= open(file_name,'a',0)

with Lepton() as l:
    a,_ = l.capture()

cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
np.right_shift(a, 8, a) # fit data into 8 bits
cv2.imwrite(time_now+'.jpg', np.uint8(a)) # write it!

b = a.ravel()
      
x_arrstr = np.char.mod('%i', b)
x_str = ",".join(x_arrstr)

fid.write(time_now+','+x_str+'\n\r')
