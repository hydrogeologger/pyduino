
in serial connection:

RESET  -- will reset raspberry pi in 21 seconds




```python
read_suction_sensor(ard,input_command="dht22,10,power,48,points,2,dummies,1,interval_mm,200,debug,1",names_address={'humidity':11,'temp_air':10},delimiter=',')
```


TO200904 It would be better not install multiple analog sensor in to one analog channel as it will be interfered by the neighbouring sensors. --- learned from redmud amphirol case study.
