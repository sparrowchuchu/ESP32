from machine import Pin,I2C
import mpu6050                # 六軸感測器
import time

i2c=I2C(scl=Pin(25),sda=Pin(26))  # SDA(串列資料線),SCL(串列時脈線)
accelerometer=mpu6050.accel(i2c)

# 過濾剛通電時的初始訊號。
while(accelerometer.get_values()['AcX']==0 and
      accelerometer.get_values()['AcY']==0 and
      accelerometer.get_values()['AcZ']==0 ):
    pass

while True:
    six_data=accelerometer.get_values()
    print(six_data)
    print(six_data['AcX'])
    time.sleep(0.5)


# button_yes=Pin(12,Pin.IN,Pin.PULL_UP)  # 儲存按鈕。FULL_UP啟動內建上拉電阻
# button_no=Pin(13,Pin.IN,Pin.PULL_UP)   # 捨棄按鈕
# 
# while True:
#     print(button_no.value(),button_yes.value())
#     time.sleep(0.1)


