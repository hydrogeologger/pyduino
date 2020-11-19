
in serial connection:

RESET  -- will reset raspberry pi in 21 seconds




```python
read_suction_sensor(ard,input_command="dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1",names_address={'humidity':11,'temp_air':10},delimiter=',')
```


TO200904 It would be better not install multiple analog sensor in to one analog channel as it will be interfered by the neighbouring sensors. --- learned from redmud amphirol case study.


TO201118 lists of commands used for version 3 datalogger

on board humidity sensor:

```
dht22,54,power,2,points,2,dummies,1,interval_mm,200,debug,1
```


Reading the onboard DC voltage (VSENSE, requiring the pins are propoerly setup)
```
analog,15,power,9,points,5,dummies,3,interval_mm,200,257.00,
```


Thermal suction sensor
```
fred,5A22A047,dgin,18,snpw,26,htpw,23,itv,6000,otno,5
```

SDI12 decagon moisture sensor:

```
SDI-12,53,power,46,default_cmd,read,debug,1
```




