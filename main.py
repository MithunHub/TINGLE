# -*- coding:utf-8 -*-
import PCF8591 as ADC
import csv
import time
import socket
import numpy as np

def map(x,in_min,in_max,out_min,out_max,compensation):
    data_raw = (x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min + compensation
    if data_raw > 0 and data_raw < 10:
        data = format(data_raw, '.4f')
    elif data_raw < 0:
        data = format(data_raw, '.3f')
    elif data_raw > 10 and data_raw < 100:
        data = format(data_raw, '.3f')
    else:
        data = format(data_raw, '.2f')
    return data

def setup():
    ADC.setup(0x48)

def loop():
    i = 0
    j = 0
    TIME = 0

    VCC = 5.0
    R_div=100000.0
    straight1 = 30114.0
    bend1 = 55800.0
    straight5 = 29500.0
    bend5 = 48500.0
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('192.168.43.51', 6666))  #绑定ip和端口号（IP为发送数据的树莓派ip，端口号自己指定）
    s.listen(5)
    c, address = s.accept()      #等待别的树莓派接入

    while True:
		#part of getting local time
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime('%Y-%m-%d %H:%M:%S',local_time)
        data_secs = (ct - int(ct)) * 1000
        time_finial = "%s.%03d" % (data_head, data_secs)

        degree1_flexV = ADC.read(0) * VCC /256
        degree1_flexR = R_div * (VCC/degree1_flexV - 1.0)
        degree1 = map(degree1_flexR,straight1,bend1,0,90.0,-11.280)

        degree2_flexV = ADC.read(1) * VCC /256
        degree2_flexR = R_div * (VCC/degree2_flexV - 1.0)
        degree2 = map(degree2_flexR,straight5,bend5,0,90.0,4.058)

        TIME = TIME + 0.5
        time.sleep(0.5)
		#mode1
        if(TIME%4 == 0):

            if(float(degree1) < 10.000 and float(degree2) < 10.000):
                
                print(time_finial, 'finger1 degree = ', degree1)
                print(time_finial, 'finger2 degree = ', degree2)
                
                msg = degree1 + ' ' + degree2
                
                c.send(msg.encode('utf-8'))   #编码
                 
                with open("test_data1.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time", "ID", "Value"])
                    writer.writerows([[time_finial, 'finger1', degree1], [time_finial, 'finger2', degree2]])

            elif(float(degree1) > 10.000 and float(degree2) > 10.000):

                print(time_finial, 'finger1 degree = ', degree1)
                print(time_finial, 'finger2 degree = ', degree2)
                
                msg = degree1 + ' ' + degree2
                
                c.send(msg.encode('utf-8'))   #编码
                
                with open("test_data1.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time", "ID", "Value"])
                    writer.writerows([[time_finial, 'finger1', degree1], [time_finial, 'finger2', degree2]])
                    
            elif(float(degree1) > 10.000 and i < 15):
                for i in range(15):
                    
                    print(time_finial, 'finger1 degree = ', degree1)
                    
                    msg = degree1 + ' ' + degree2
                    
                    c.send(msg.encode('utf-8'))   #编码
                    
                    with open("test_data1.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Time", "ID", "Value"])
                        writer.writerows([[time_finial, 'finger1',degree1]])
                        
                i = 0
                             
                print(time_finial, 'finger2 degree = ', degree2)
                
                msg = degree1 + ' ' + degree2
                    
                c.send(msg.encode('utf-8'))   #编码
                
                with open("test_data1.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time", "ID", "Value"])
                    writer.writerows([[time_finial, 'finger2',degree2]])
                    
            elif(float(degree2) > 10.000 and j < 15):
                for j in range(15):
                    
                    print(time_finial, 'finger2 degree = ', degree2)
                    
                    msg = degree1 + ' ' + degree2
                        
                    c.send(msg.encode('utf-8'))   #编码
                    
                    with open("test_data1.csv", "a") as csvfile:
                        writer = csv.writer(csvfile)
                        writer.writerow(["Time", "ID", "Value"])
                        writer.writerows([[time_finial, 'finger2',degree2]])
                        
                j = 0
                
                print(time_finial, 'finger1 degree = ', degree1)
                
                msg = degree1 + ' ' + degree2
                    
                c.send(msg.encode('utf-8'))   #编码
                
                with open("test_data1.csv", "a") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Time", "ID", "Value"])
                    writer.writerows([[time_finial, 'finger1',degree1]])
                    
            else:
                print("Warning! The data is missing")

		#mode2
            '''elif(TIME%2 == 0):

			if(float(degree1) < 10.000 and float(degree2) < 10.000):
				print(time_finial, 'finger1 degree = ', degree1)
				print(time_finial, 'finger2 degree = ', degree2)
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger1', degree1], [time_finial, 'finger2', degree2]])


			elif(float(degree1) > 10.000 and float(degree2) > 10.000):
				print(time_finial, 'finger1 degree = ', degree1)
				print(time_finial, 'finger2 degree = ', degree2)
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger1', degree1], [time_finial, 'finger2', degree2]])
			elif(float(degree1) > 10.000 and i < 15):
				print(time_finial, 'finger1 degree = ', degree1)
				i = i + 1
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger1',degree1]])
			elif(float(degree1) > 10.000 and i == 15):
				print(time_finial, 'finger2 degree = ', degree2)
				i = 0
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger2',degree2]])
			elif(float(degree2) > 10.000 and j < 15):
				print(time_finial, 'finger2 degree = ', degree2)
				j = j + 1
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger2',degree2]])
			elif(float(degree2) > 10.000 and j == 15):
				print(time_finial, 'finger1 degree = ', degree1)
				j = 0
				with open("test_data1.csv", "a") as csvfile:
					writer = csv.writer(csvfile)
					writer.writerow(["Time", "ID", "Value"])
					writer.writerows([[time_finial, 'finger1',degree1]])
			else:
				print("Warning! The data is missing")


			for i in range(2):
				if(i == 0):
					print(time_finial, 'finger1 degree = ', degree1)
				else:
					print(time_finial, 'finger2 degree = ', degree2)
			with open("test_data1.csv","a") as csvfile:
				writer = csv.writer(csvfile)
				writer.writerow(["Time","ID","Value"])
				writer.writerows([[time_finial,'finger1',degree1],[time_finial,'finger2',degree2]])
				'''

		#mode3
        else:

            for i in range(2):
                if(i == 0):
                    
                    print(time_finial, 'finger1 degree = ', degree1)
                    
                    msg = degree1 + ' ' + degree2
                        
                    c.send(msg.encode('utf-8'))   #编码
                    
                else:

                    print(time_finial, 'finger2 degree = ', degree2)
                    
                    msg = degree1 + ' ' + degree2
                        
                    c.send(msg.encode('utf-8'))   #编码
                    
            with open("test_data1.csv","a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Time","ID","Value"])
                writer.writerows([[time_finial,'finger1',degree1],[time_finial,'finger2',degree2]])


  #打印电位计电压大小A/D转换后的数字值（从AIN0借口输入的）
  #范围是0~255,0时LED灯熄灭，255时灯最亮

  #将0通道输入的电位计电压数字值转化成模拟值从AOUT输出
  #给LED灯提供电源VCC输入

def destroy():
	ADC.write(0)

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
