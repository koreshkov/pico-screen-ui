# Pico Screen UI

A MicroPython UI framework for Raspberry Pi Pico with display.

## Features

- Multiple screen types (Home, Settings, Files browser, Selection lists)
- Digital and analog clock display
- Customizable color palette
- File system navigation
- Button-based navigation with debouncing
- WiFi connectivity support
- Weather data integration (Open-Meteo API)

## Configuration

Edit `config.py` to set your credentials and preferences:

```python
WIFI_SSID = 'your_network_name'
WIFI_PASSWORD = 'your_password'
WEATHER_LAT = 55.676098  # Your latitude
WEATHER_LNG = 12.568337  # Your longitude
```

## Project Structure

- `main.py` - Entry point
- `config.py` - Configuration settings
- `ui.py` - Main UI controller and button handling
- `ui_screen.py` - Screen classes (Home, Settings, Files, etc.)
- `wifi.py` - WiFi connection handler
- `weather.py` - Weather data fetcher
- `libs/` - Additional libraries

## Hardware Requirements

- Raspberry Pi Pico
- Pico Display 2.0 (320x240 LCD)
- 4 buttons connected to GPIO pins 12-15

## Usage

Simply upload the files to your Pico and run `main.py`. The UI will start automatically and connect to WiFi.

### Navigation

- Button A: Navigate up/go to Files
- Button B: Navigate down/go to Settings
- Button X: Go back
- Button Y: Select/confirm
