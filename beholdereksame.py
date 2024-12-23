from machine import Pin, ADC, PWM, SoftI2C
import dht
import ssd1306
import time

dht_sensor = dht.DHT11(Pin(4)) 
IN1 = PWM(Pin(16), freq=1000)   
IN2 = PWM(Pin(17), freq=1000)   

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))  
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

def køl():
    IN1.duty(1023) 
    IN2.duty(0)

def varm():
    IN1.duty(0)     
    IN2.duty(1023)

def stop():
    IN1.duty(0)     
    IN2.duty(0)

min_temp = 25 
max_temp = 30 

while True:
    try:
        dht_sensor.measure()
        temp = dht_sensor.temperature()

        if temp < min_temp:
            varm()
        elif temp > max_temp:
            køl()
        else:
            stop()

        oled.fill(0)
        oled.text("Temp: {}C".format(temp), 0, 0)
        if temp < min_temp:
            oled.text("Opvarmning...", 0, 20)
        elif temp > max_temp:
            oled.text("Koeler...", 0, 20)
        else:
            oled.text("Stabil.", 0, 20)
        oled.show()

        time.sleep(1) 

    except Exception as e:
        print("Fejl: ", e)
        oled.fill(0)
        oled.text("Fejl: {}".format(str(e)), 0, 0)
        oled.show()
        time.sleep(5)