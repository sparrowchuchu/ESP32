from machine import Pin,I2C
import mpu6050                # 六軸感測器
import time
from keras_lite import Model
import ulab as np

mean= 2225.221962962963
std= 11163.010533919562

model=Model('gesture_model.json')
label_name=['right','down','stop','left','up']

button=Pin(12,Pin.IN,Pin.PULL_UP)
i2c=I2C(scl=Pin(25),sda=Pin(26))       # SDA(串列資料線),SCL(串列時脈線)
accelerometer=mpu6050.accel(i2c)

# 過濾剛通電時的初始訊號。
while(accelerometer.get_values()['AcX']==0 and
      accelerometer.get_values()['AcY']==0 and
      accelerometer.get_values()['AcZ']==0 ):
    pass

print('開始')

while True:
    data=[]
    
    if(button.value()==0):
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
        
        while(button.value()==0):
            pass
        
        time.sleep(0.01)











