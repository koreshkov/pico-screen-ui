# Base screen

class UIScreen:

    def __init__(self, name, ui):
        self.name = name
        self.ui = ui
        self.display = ui.display
        self.palette = ui.palette
    
    def init(self):
        pass
    
    def deinit(self):
        pass
    
    def clear(self):
        self.display.set_pen(self.palette.secondary)
        self.display.clear()
    
    def update(self):
        pass
    
    def render(self, tim=None):
        pass
    
    def render_labels(self, labels: list):
        positions = [
            (True, True),      # A button (top-left)
            (True, False),     # B button (bottom-left)
            (False, True),     # X button (top-right)
            (False, False)     # Y button (bottom-right)
        ]
        
        for i, (is_left, is_top) in enumerate(positions):
            if i < len(labels) and labels[i]:
                text = labels[i]
                width = self.display.measure_text(text, 2)
                x = 0 if is_left else self.ui.width - width - 12
                y = 0 if is_top else self.ui.height - 24
                
                self.display.set_pen(self.palette.primary)
                self.display.rectangle(x, y, width + 12, 24)
                self.display.set_pen(self.palette.secondary)
                self.display.text(text, x + 6, y + 6, self.ui.width, 2)

    def btn_a_handler(self):
        print(f'{self.name}: A')
    
    def btn_b_handler(self):
        print(f'{self.name}: B')
    
    def btn_x_handler(self):
        print(f'{self.name}: X')
    
    def btn_y_handler(self):
        print(f'{self.name}: Y')