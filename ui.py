from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4  # type: ignore
import time
from machine import Pin
from screen.home import UIHomeScreen
from screen.settings import UISettingsScreen
from screen.network import UINetworkScreen
from screen.select import UISelectScreen
from screen.files import UIFilesScreen
from screen.pong import UIPongScreen
from config import DISPLAY_BACKLIGHT, DEBOUNCE_DELAY

# Display

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, pen_type=PEN_P4, rotate=0)
display.set_backlight(DISPLAY_BACKLIGHT)
display.set_font("bitmap6")

# Colors

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(255, 0, 0)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
CYAN = display.create_pen(0, 255, 255)
BLUE = display.create_pen(0, 0, 255)
MAGENTA = display.create_pen(255, 0, 255)

# Palette

class Palette:
    """Color palette manager for the UI."""
    
    def __init__(self, colors, primary=4, secondary=0):
        self.colors = colors
        self._primary = primary
        self._secondary = secondary
    
    @property
    def primary(self):
        return self.colors[self._primary][1]
    
    @primary.setter
    def primary(self, primary):
        self._primary = primary
    
    @property
    def secondary(self):
        return self.colors[self._secondary][1]
    
    @secondary.setter
    def secondary(self, secondary):
        self._secondary = secondary

palette_colors = [
    ('BLACK', BLACK),
    ('WHITE', WHITE),
    ('RED', RED),
    ('YELLOW', YELLOW),
    ('GREEN', GREEN),
    ('CYAN', CYAN),
    ('BLUE', BLUE),
    ('MAGENTA', MAGENTA)
]

palette = Palette(palette_colors)

# UI

class UI:
    """Main UI controller managing screens and button handlers."""
    
    def __init__(self, display, palette):
        self.display = display
        self.width, self.height = display.get_bounds()
        self.palette = palette
        self.clock_type = 0
        # Dictionary to store screens by name
        self.screens = {}
        # List to maintain screen order
        self.screen_order = []
        self._add_screen(UIHomeScreen('HOME', self))
        self._add_screen(UIFilesScreen('FILES', self))
        self._add_screen(UISettingsScreen('SETTINGS', self, [
            ('Clock', 0),
            ('Colors', 1),
            ('Test #2', 2),
            ('Test #3', 3),
            ('Test #4', 4),
            ('Test #5', 5),
            ('Test #6', 2),
            ('Test #7', 3),
            ('Test #8', 4),
            ('Test #9', 5),
            ('Test #10', 2),
            ('Test #11', 3),
            ('Test #12', 4),
            ('Test #13', 5),
            ('Test #14', 5),
            ('Test #15', 2),
            ('Test #16', 3),
            ('Test #17', 4),
            ('Test #18', 5)
        ], self.on_setting_select))
        self._add_screen(UINetworkScreen('NETWORK', self))
        self._add_screen(UISelectScreen('CLOCK', self, [('Digital', 0), ('Analog', 1)], self.clock_type, self.on_clock_select))
        self._add_screen(UISelectScreen('COLORS', self, [(color[0], idx) for idx, color in enumerate(self.palette.colors)], self.palette.primary, self.on_color_select))
        self._add_screen(UIPongScreen('PONG', self))
        self.active_screen = self.screen_order[0]
        self.screens[self.active_screen].init()

    def _add_screen(self, screen):
        """Add a screen to the UI by name."""
        screen_name = screen.name
        self.screens[screen_name] = screen
        self.screen_order.append(screen_name)

    def get_active_screen(self):
        return self.screens[self.active_screen]

    def set_active_screen(self, screen_name):
        """Switch to a screen by name or index.
        
        Args:
            screen_name: Screen name (str) or index (int)
        """
        # Support both name and index for backwards compatibility
        if isinstance(screen_name, int):
            screen_name = self.screen_order[screen_name]
        
        if screen_name not in self.screens:
            raise ValueError(f"Screen '{screen_name}' not found")
        
        active_screen = self.get_active_screen()
        active_screen.deinit()
        self.active_screen = screen_name
        active_screen = self.get_active_screen()
        active_screen.init()

    # UPDATE
    
    def update(self):
        self.get_active_screen().update()

    # BUTTON ACTIONS
    
    def btn_a_handler(self, p = None):
        self.get_active_screen().btn_a_handler()
    
    def btn_b_handler(self, p = None):
        self.get_active_screen().btn_b_handler()
    
    def btn_x_handler(self, p = None):
        self.get_active_screen().btn_x_handler()
    
    def btn_y_handler(self, p = None):
        self.get_active_screen().btn_y_handler()
    
    # SCREEN SELECT ACTIONS
    
    def on_setting_select(self, value):
        if value == 0:
            self.set_active_screen('CLOCK')
        elif value == 1:
            self.set_active_screen('COLORS')

    def on_clock_select(self, value):
        self.clock_type = value
        
    def on_color_select(self, value):
        self.palette.primary = value
        self.palette.secondary = 1 if value == 0 else 0

def init_ui() -> UI:
    ui = UI(display, palette)
    return ui
        
# Button setup

def create_button_handler(pin_number, handler_func):
    btn = Pin(pin_number, Pin.IN, Pin.PULL_UP)
    
    def handler(pin):
        btn.irq(handler=None)
        handler_func()
        time.sleep(DEBOUNCE_DELAY)
        btn.irq(handler=handler)
    
    btn.irq(handler, Pin.IRQ_FALLING)
    return btn

def init_ui_buttons(ui_instance: UI):
    create_button_handler(12, ui_instance.btn_a_handler)
    create_button_handler(13, ui_instance.btn_b_handler)
    create_button_handler(14, ui_instance.btn_x_handler)
    create_button_handler(15, ui_instance.btn_y_handler)

# Initialize button interrupts
# btnA = create_button_handler(12, myUI.btn_a_handler)
# btnB = create_button_handler(13, myUI.btn_b_handler)
# btnX = create_button_handler(14, myUI.btn_x_handler)
# btnY = create_button_handler(15, myUI.btn_y_handler)