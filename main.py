"""
Main entry point for Pico Screen UI application.
Initializes WiFi connection and starts the UI.
"""
import wifi
from ui import init_ui, init_ui_buttons

pico_ui = init_ui()
init_ui_buttons(pico_ui)

# Initialize WiFi connection
wlan = wifi.connect()

# Main loop - continuously update active screen
# This allows screens like Pong to animate while still
# responding to button interrupts
while True:
    pico_ui.update()