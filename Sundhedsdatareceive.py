import network
import espnow
import urequests 
import time
import ujson  

wlan = None

def connect_to_wifi(ssid, password):
    global wlan  
    wlan = network.WLAN(network.STA_IF) 
    wlan.active(True)
    if not wlan.isconnected():
        print("Forbinder til WiFi...")
        wlan.connect(ssid, password)  
        while not wlan.isconnected():
            time.sleep(1)
    print("WiFi forbundet!")
    print("IP-adresse:", wlan.ifconfig()[0])  

def setup_espnow():
    esp = espnow.ESPNow()
    esp.active(True)
    return esp

def send_to_server(data):
    global wlan 
    message = data  
    url = "http://192.168.1.100:5000/api/data" 
    
    payload = ujson.dumps({"message": message})  
    headers = {"Content-Type": "application/json"}

    if not wlan.isconnected():
        print("WiFi tabt. Genopretter forbindelse...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
        print("WiFi forbundet igen!")

    try:
        print("Sender data til server...")
        response = urequests.post(url, data=payload, headers=headers, timeout=5)  # Send som raw JSON string
        print("Server Response:", response.text)
        response.close()
    except Exception as e:
        print("Fejl ved sending til server:", e)

def main():
    global ssid, password  
    ssid = "IoT-4"
    password = "Password!"

    connect_to_wifi(ssid, password)

    esp = setup_espnow()

    print("Venter på data fra ESP-NOW...")
    while True:
        peer, msg = esp.recv()
        if msg:  
            decoded_msg = msg.decode()
            print(f"Modtaget fra {peer}: {decoded_msg}")
            send_to_server(decoded_msg)  
main()