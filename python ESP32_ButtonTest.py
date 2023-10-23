from machine import Pin
# import mpu6050                # 六軸感測器
import time


button_yes=Pin(12,Pin.IN,Pin.PULL_UP)  # 儲存按鈕。FULL_UP啟動內建上拉電阻
button_no=Pin(13,Pin.IN,Pin.PULL_UP)   # 捨棄按鈕

while True:
    print(button_no.value(),button_yes.value())
    time.sleep(0.1)



