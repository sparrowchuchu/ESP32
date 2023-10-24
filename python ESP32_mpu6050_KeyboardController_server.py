# 伺服器端(ESP32)
from machine import I2C, Pin
import machine
import mpu6050
import time
from keras_lite import Model
import ulab as np
import network
import socket          # Socket是一種網路通訊的API

host='0.0.0.0'         # IP位置。0.0.0.0代表任意IP
port=9999              # 通訊埠編號

mean= 2225.221962962963
std= 11163.010533919562

model = Model('gesture_model.json')  
label_name = ['right','down','stop','left','up']

LED=Pin(2,Pin.OUT,value=0)  # 關閉內鍵led燈

button=Pin(12,Pin.IN,Pin.PULL_UP)      # FULL_UP啟動內建上拉電阻
button_e=Pin(13,Pin.IN,Pin.PULL_UP)
i2c=I2C(scl=Pin(25),sda=Pin(26))       # SDA(串列資料線),SCL(串列時脈線)
accelerometer=mpu6050.accel(i2c)

while(accelerometer.get_values()['AcX']==0 and
      accelerometer.get_values()['AcY']==0 and
      accelerometer.get_values()['AcZ']==0):
    pass

sta=network.WLAN(network.STA_IF)   # STA (station 站台)
sta.active(True)                   # 啟用網路介面
sta.connect('a347','34716385')     # 連線至WiFi
while(not sta.isconnected()):
    pass
# print('IP位址:',sta.ifconfig()[0])

LED.value(1)           # 連上WiFi時亮燈

ap=network.WLAN(network.AP_IF)     # AP (access point 熱點)
ap.active(True)
ap.config(essid='ESP-'+str(sta.ifconfig()[0]))  # AP名稱為IP位址

sock=socket.socket()
sock.bind((host,port)) # 使用指定IP和通訊埠進行綁定
sock.listen(1)         # 最大連接量
# print('等待客戶端連線')

(csock,adr)=sock.accept()
# print(adr)
# print('客戶端已連線')

while True:
    while(not sta.isconnected()):
        LED.value(0)          # 沒連上WiFi時亮燈
    LED.value(1)              # 連上WiFi時亮燈
    
    data=[]                   # 重製data
     
    if(button.value()==0):    # 按下按鈕 
        for i in range(10):
            six_data=accelerometer.get_values()
                
            data.append(six_data['AcX'])  # 加速度計 x 軸
            data.append(six_data['AcY'])  # 加速度計 y 軸
            data.append(six_data['AcZ'])  # 加速度計 z 軸
            data.append(six_data['GyX'])  # 陀螺儀 x 軸
            data.append(six_data['GyY'])  # 陀螺儀 y 軸
            data.append(six_data['GyZ'])  # 陀螺儀 z 軸
        
        data=np.array([data])
        data=(data-mean)/std
        output=model.predict_classes(data)
        direction=label_name[output[0]]
        print(direction)
        
        while(button.value()==0): # 等待放開按鈕
            pass
        csock.send(direction)     # 發出[方向]訊號            
        time.sleep(0.1)           # 稍微暫停一下
        
    elif(button_e.value()==0):    # 按下按鈕
        while(button.value()==0): # 等待放開按鈕
            pass
        csock.send(b'enter')      # 發出[方向]訊號            
        time.sleep(0.1)           # 稍微暫停一下

sock.close()                      # 關閉socket

