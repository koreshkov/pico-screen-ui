"""
WiFi connection handler for Pico.
"""
from time import sleep
import network
from config import WIFI_SSID, WIFI_PASSWORD


def connect():
    """
    Connect to WiFi network using credentials from config.
    
    Returns:
        wlan: Connected WLAN interface object
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    
    while not wlan.isconnected():
        print('Waiting for connection...')
        sleep(1)

    ip = wlan.ifconfig()[0]
    print(f'Connected! IP: {ip}')
    
    return wlan
