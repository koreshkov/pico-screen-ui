"""
Main entry point for Pico Screen UI application.
Initializes WiFi connection and starts the UI.
"""
import wifi
from ui import myUI

# Initialize WiFi connection
wlan = wifi.connect()

# Main loop - continuously update active screen
# This allows screens like Pong to animate while still
# responding to button interrupts
while True:
    myUI.update()