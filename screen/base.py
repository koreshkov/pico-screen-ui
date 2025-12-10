"""UI Screen classes for different application views."""



# Generic screen

class UIScreen:
    """Base class for all UI screens."""
    
    def __init__(self, name, ui):
        self.name = name
        self.ui = ui
        self.display = ui.display
        self.palette = ui.palette
    
    def init(self):
        """Called when screen becomes active."""
        pass
    
    def deinit(self):
        """Called when screen becomes inactive."""
        pass
    
    def clear(self):
        """Clear the display with secondary color."""
        self.display.set_pen(self.palette.secondary)
        self.display.clear()
    
    def update(self):
        """Update screen state - called continuously by main loop."""
        pass
    
    def render(self):
        """Render the screen content."""
        pass
    
    def btn_a_handler(self):
        print(f'{self.name}: A')
    
    def btn_b_handler(self):
        print(f'{self.name}: B')
    
    def btn_x_handler(self):
        print(f'{self.name}: X')
    
    def btn_y_handler(self):
        print(f'{self.name}: Y')
    
# Home screen



# List item


# Settings screen



# Select list



# Files screen

