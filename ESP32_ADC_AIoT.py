from machine import Pin,ADC
import time
from keras_lite import Model
import ulab as np  # MicroPython中沒有Numpy模組
import network
import urequests

# 連線至網路
sta=network.WLAN(network.STA_IF)
sta.active(True)
sta.connect('無線網路名稱','無線網路密碼')

while not sta.isconnected():
    pass

print('Wifi連線成功')

device_id='請填入中華電信設備編號'
headers={'CK':'請填入中華電信設備金鑰'}

# 中華電信IoT平台
url_CHT='http://iot.cht.com.tw/iot/v1/device/'\
         +device_id+'/rawdata'

mean=170.98275862068965
std=90.31162360353873
model=Model('temperature_model.jason')

adc_pin=Pin(36)    # 36是ESP32的VP腳位。使用腳位VP當作類比腳位。
adc=ADC(adc_pin)   # 建立ADC物件
adc.width(ADC.WIDTH_9BIT)  # 設定ADC範圍。9BIT代表範圍是 0~511。
adc.atten(ADC.ATTN_11DB)   # 將最大感測電壓設定成 3.6V。

data=0

while True:
    num=20                 # 每幾筆資料平均一次
    for i in range(num):
        thermal=adc.read()
        data+=thermal
        time.sleep(0.1)    # 暫停0.5秒

    data=data/num
    data=np.array([int(data)])
    data-=mean
    data/=std
    tem=model.predict(date)
    tem=round(tem[0]*100,1)
    print(tem,end='   ')
    
    CHT_data=[{'id':'請填入中華電信感測器編號','value':[str(tem)]}]
    
    urequests.post(url_CHT,json=CHT_data, # 上傳資料
                   headers=headers)
    print('上傳完畢')
    data=0
    time.sleep(60)        # 暫停60秒


