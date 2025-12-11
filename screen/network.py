"""Network connection details screen."""
import network
from machine import Timer
from screen.base import UIScreen


class UINetworkScreen(UIScreen):
    """Screen displaying network connection details."""
    
    def __init__(self, name, ui):
        super().__init__(name, ui)
        self.rtc_timer = None
    
    def init(self):
        """Called when screen becomes active."""
        self.render()
        self.rtc_timer = Timer(mode=Timer.PERIODIC, period=1000, callback=self.render)
    
    def deinit(self):
        """Called when screen becomes inactive."""
        if self.rtc_timer:
            self.rtc_timer.deinit()
    
    def get_network_info(self):
        """Get network connection details."""
        try:
            wlan = network.WLAN(network.STA_IF)
            
            if not wlan.active():
                return {
                    'status': 'WiFi Disabled',
                    'ssid': '-',
                    'ip': '-',
                    'netmask': '-',
                    'gateway': '-',
                    'dns': '-',
                    'mac': '-',
                    'rssi': '-'
                }
            
            if not wlan.isconnected():
                mac = ':'.join(f'{b:02x}' for b in wlan.config('mac'))
                return {
                    'status': 'Not Connected',
                    'ssid': '-',
                    'ip': '-',
                    'netmask': '-',
                    'gateway': '-',
                    'dns': '-',
                    'mac': mac,
                    'rssi': '-'
                }
            
            ifconfig = wlan.ifconfig()
            mac = ':'.join(f'{b:02x}' for b in wlan.config('mac'))
            
            try:
                rssi = wlan.status('rssi')
            except:
                rssi = 'N/A'
            
            return {
                'status': 'Connected',
                'ssid': wlan.config('essid'),
                'ip': ifconfig[0],
                'netmask': ifconfig[1],
                'gateway': ifconfig[2],
                'dns': ifconfig[3],
                'mac': mac,
                'rssi': f'{rssi} dBm' if rssi != 'N/A' else 'N/A'
            }
        except Exception as e:
            return {
                'status': f'Error: {str(e)}',
                'ssid': '-',
                'ip': '-',
                'netmask': '-',
                'gateway': '-',
                'dns': '-',
                'mac': '-',
                'rssi': '-'
            }
    
    def render(self, tim=None):
        """Render the network details screen."""
        self.clear()
        
        info = self.get_network_info()
        
        # Title
        title = 'NETWORK INFO'
        self.display.set_pen(self.palette.primary)
        self.display.text(title, 10, 10, 320, 3)
        
        # Network details
        y_pos = 50
        line_height = 20
        label_x = 10
        value_x = 120
        
        details = [
            ('Status:', info['status']),
            ('SSID:', info['ssid']),
            ('IP Address:', info['ip']),
            ('Netmask:', info['netmask']),
            ('Gateway:', info['gateway']),
            ('DNS:', info['dns']),
            ('MAC:', info['mac']),
            ('Signal:', info['rssi'])
        ]
        
        for label, value in details:
            self.display.set_pen(self.palette.primary)
            self.display.text(label, label_x, y_pos, 320, 2)
            self.display.text(value, value_x, y_pos, 320, 2)
            y_pos += line_height
        
        # Render labels
        self.render_labels([None, None, 'BACK', None])
        
        self.display.update()
    
    def btn_a_handler(self):
        """Button A handler."""
        print(f'{self.name}: A')
    
    def btn_b_handler(self):
        """Button B handler."""
        print(f'{self.name}: B')
    
    def btn_x_handler(self):
        """Button X handler - go back."""
        self.ui.set_active_screen('HOME')
    
    def btn_y_handler(self):
        """Button Y handler."""
        print(f'{self.name}: Y')
