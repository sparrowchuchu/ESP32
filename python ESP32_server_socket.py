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
port=6543              # 可使用通訊埠編號範圍: 1024~65535

sock=socket.socket()
sock.bind((host,port)) # 使用指定IP和通訊埠進行綁定
sock.listen(1)         # 最大連接量
print('等待客戶端連線')

(csock,adr)=sock.accept()
print(adr)
print('客戶端已連線')


print('IP位址:',sta.ifconfig()[0])

csock.send('abc')             

# sock.close()                      # 關閉socket



