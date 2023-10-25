from machine import Pin,I2C
import mpu6050                # 六軸感測器
import time

button_yes=Pin(12,Pin.IN,Pin.PULL_UP)  # 儲存按鈕。FULL_UP啟動內建上拉電阻
#button_no=Pin(13,Pin.IN,Pin.PULL_UP)   # 捨棄按鈕
i2c=I2C(scl=Pin(25),sda=Pin(26))       # SDA(串列資料線),SCL(串列時脈線)
accelerometer=mpu6050.accel(i2c)

f=open('up.txt','w')

# 過濾剛通電時的初始訊號。
while(accelerometer.get_values()['AcX']==0 and
      accelerometer.get_values()['AcY']==0 and
      accelerometer.get_values()['AcZ']==0 ):
    pass

data=[]
reset=False

# 儲存100筆
for j in range(100):
    print('\n第'+str(j+1)+'筆,可以開始動作:')
    data=[]
    
    while True:
        # 如果是第一筆或上一筆資料剛結束時，初始化六軸的值。
        if(button_yes.value()==0):           # 按下按鈕       
            for i in range(10):               # 收集10次6軸數值
                six_data=accelerometer.get_values()
                
                data.append(six_data['AcX'])  # 加速度計 x 軸
                data.append(six_data['AcY'])  # 加速度計 y 軸
                data.append(six_data['AcZ'])  # 加速度計 z 軸
                data.append(six_data['GyX'])  # 陀螺儀 x 軸
                data.append(six_data['GyY'])  # 陀螺儀 y 軸
                data.append(six_data['GyZ'])  # 陀螺儀 z 軸
                time.sleep(0.01)
            
            f.write(str(data)[1:-1]+'\n')
            print('Save')
            while(button_yes.value()==0):         # 等待放開按鈕
                pass
            time.sleep(0.1)
            break
        
f.close()
print('完成資料蒐集。')


