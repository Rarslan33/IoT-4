import network
import espnow
import time
import dht
from machine import Pin

SSID = "IoT-4" 
PASSWORD = "Password!" 

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Tilslutter til router...")
wlan.connect(SSID, PASSWORD)

while not wlan.isconnected():
    print("Venter på Wi-Fi forbindelse...")
    time.sleep(1)

print("Forbundet til router!")
print("IP:", wlan.ifconfig()[0])

esp = espnow.ESPNow()
esp.active(True)

peer_mac = b'\xcc\xdb\xa7\x95\x50\xbc'  
esp.add_peer(peer_mac)

sensor = dht.DHT11(Pin(4))

def send_sensor_data():
    try:
        sensor.measure() 
        temperature = sensor.temperature() 

        if temperature > 30:  
            message = "Højt blodtryk!"
        else:
            message = "Blodtryk er normalt"

        print(f"Sender: {message}")
        esp.send(peer_mac, message) 

    except OSError as e:
        print(f"Fejl ved sensor aflæsning: {e}")

while True:
    send_sensor_data()
    time.sleep(10)  