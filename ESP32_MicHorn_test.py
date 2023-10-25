from machine import Pin,ADC,PWM
import time

# 工作週期duty: 設定為0(範圍0~1023)。PWM預設duty為512
# 頻率freq: 設定為6000。PWM預設freq為5000
horn=PWM(Pin(14),duty=0,freq=6000)

button_yes=(Pin(12),Pin.IN,Pin.PULL_PU)

adc=ADC(Pin(36))
adc.width(ADC.WIDTH_12BIT)     # 解析度12BT
adc.atten(ADC.ATTN_11DB)       # 最大電壓36V

while True:
    if button_yes.value()==0:  # 當按下按鈕
        data=[]
        print('action')
        
        # 蒐集聲音
        while button_yes.value()==0 and len(data)<=1200:
            data.append(adc.read())
            time.sleep_us(167) # 延遲167微秒(0.000167秒)
            
        # 播放音效
        for j in data:
            horn.duty(int(j/4))
            time.sleep_us(167)
        horn.duty(0)           # 關閉喇叭聲音
        
    time.sleep(0.01)


