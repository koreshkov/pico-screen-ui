from machine import RTC, Timer
from screen.base import UIScreen
import network
import math

rtc = RTC()

class UIHomeScreen(UIScreen):
    
    def __init__(self, name, ui):
        super().__init__(name, ui)
        self.rtc = rtc
    
    def get_ip_address(self):
        try:
            wlan = network.WLAN(network.STA_IF)
            if wlan.isconnected():
                return wlan.ifconfig()[0]
            else:
                return 'no wifi'
        except:
            return 'no wifi'
    
    def init(self):
        self.render()
        self.rtc_timer = Timer(mode=Timer.PERIODIC, period=1000, callback=self.render)
    
    def deinit(self):
        self.rtc_timer.deinit()

    def render(self, tim=None):
        self.clear()
        
        self.render_clock()

        labels = ['FILES', 'SETTINGS', self.get_ip_address(), 'GAME']

        self.render_labels(labels)
        
        self.display.update()

    def render_clock(self):
        if self.ui.clock_type == 0:
            self.render_clock_digital()
        else:
            self.render_clock_analog()

    def render_clock_digital(self):
        ct = self.rtc.datetime()
        unit = 6
        font_scale = 8
        ct_hours = f'{ct[4]:02d}'
        ct_minutes = f'{ct[5]:02d}'
        ct_seconds = f'{ct[6]:02d}'
        self.display.set_pen(self.palette.primary)
        self.display.text(f'{ct_hours}:{ct_minutes}:{ct_seconds}', 12, int((240 - unit * font_scale) / 2), 320, font_scale)

    def render_clock_analog(self):
        ct = self.rtc.datetime()
        cx = 160
        cy = 120
        cr = 100
        self.display.set_pen(self.palette.primary)
        self.display.circle(cx, cy, cr)
        self.display.set_pen(self.palette.secondary)
        self.display.circle(cx, cy, cr - 2)
        self.display.set_pen(self.palette.primary)
        for a in [0, 30, 60, 90, 120, 150]:
            dx = int(cr * math.cos(math.radians(a - 90)))
            dy = int(cr * math.sin(math.radians(a - 90)))
            self.display.line(cx + dx, cy + dy, cx - dx, cy - dy)
        self.display.set_pen(self.palette.secondary)
        self.display.circle(cx, cy, cr - 10)
        self.display.set_pen(self.palette.primary)
        # seconds
        slen = 80
        srad = math.radians(ct[6] * 6 - 90)
        sx = cx + int(slen * math.cos(srad))
        sy = cy + int(slen * math.sin(srad))
        self.display.line(cx, cy, sx, sy)
        # minutes
        mlen = 70
        mrad = math.radians((ct[5] + ct[6]/60)* 6 - 90)
        mx = cx + int(mlen * math.cos(mrad))
        my = cy + int(mlen * math.sin(mrad))
        self.display.line(cx, cy, mx, my)
        # hours
        hl = 50
        hrad = math.radians((ct[4] + ct[5]/60) * 30 - 90)
        hx = cx + int(hl * math.cos(hrad))
        hy = cy + int(hl * math.sin(hrad))
        self.display.line(cx, cy, hx, hy)
        pass

    def btn_a_handler(self):
        self.ui.set_active_screen('FILES')

    def btn_b_handler(self):
        self.ui.set_active_screen('SETTINGS')

    def btn_x_handler(self):
        self.ui.set_active_screen('NETWORK')

    def btn_y_handler(self):
        self.ui.set_active_screen('PONG')