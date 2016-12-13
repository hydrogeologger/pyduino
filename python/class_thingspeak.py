import numpy as np
import httplib, urllib

def ts_upload(temp,key1):
    while True:
        fields={}
        for i in np.arange(len(temp))+1:
            fields['field'+str(i)]=temp[i-1]
        fields['key']=key1
        params = urllib.urlencode(fields)
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print response.status, response.reason
            data = response.read()
            conn.close()
        except:
            print "connection failed"
        break
