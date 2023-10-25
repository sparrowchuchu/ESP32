from machine import Pin,ADC
import time

adc_pin=Pin(36)    # 36是ESP32的VP腳位。使用腳位VP當作類比腳位。
adc=ADC(adc_pin)   # 建立ADC物件

adc.width(ADC.WIDTH_9BIT)  # 設定ADC範圍。9BIT代表範圍是 0~511。
adc.atten(ADC.ATTN_11DB)   # 將最大感測電壓設定成 3.6V。

data=0
ti=1
f=open('temperature.txt','w')

print('ADC: ',adc.read())  # 顯示ADC值,若為0或511表示接線錯誤。

while True:
    print('第'+str(ti)+'筆')
    tem=input('輸入現在溫度: ')
    
    if (tem=='end'):
        break
    else:
        num=20                 # 每幾筆資料平均一次
        for i in range(num):
            thermal=adc.read()
            data+=thermal
            time.sleep(0.1)    # 暫停0.5秒

        data=int(data/num)
        print('熱敏電阻: ',data,'/n')
        f.write(str(data)+' '+tem+'\n')
        
        data=0
        ti+=1
f.close()
