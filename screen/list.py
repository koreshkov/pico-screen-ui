from screen.base import UIScreen

class UIListItem:
    """Represents an item in a list screen."""
    
    def __init__(self, label='empty', value=None, is_active=False, is_selected=False, on_select=None):
        self.label = label
        self.value = value
        self.is_active = is_active
        self.is_selected = is_selected
        self.on_select = on_select

# List screen

class UIListScreen(UIScreen):
    """Base class for scrollable list screens."""
    
    def __init__(self, name, ui, on_select=None):
        super().__init__(name, ui)
        self.list = ['-- list is empty --']
        self.active_item = 0
        self.list_offset = 0
        self.on_select = on_select
    
    def init(self):
        self.render()
    
    def deinit(self):
        pass
    def render(self):
        list = self.get_list_for_render()
        unit = 6
        padding_scale = 1
        padding = unit * padding_scale
        font_scale = 2
        font = unit * font_scale
        scroll_threshold = 2

        item_width = self.ui.width - 24
        item_height = (font + 2 * padding)
        
        items_on_screen = 10
        items_in_list = len(list)
        if items_in_list < items_on_screen:
            items_in_list = items_on_screen
        
        if self.active_item == 0:
            self.list_offset = 0
        elif self.active_item == items_in_list - 1:
            self.list_offset = items_on_screen - items_in_list
        else:
            items_above = self.active_item + self.list_offset
            
            if items_above < scroll_threshold:
                self.list_offset += 1
                
            if items_above > items_on_screen - 1 - scroll_threshold:
                self.list_offset -= 1
            
                
    #         if active_item_offset_bottom:
            
    #         if active_item_offset_top > 7:
    #             self.list_offset = 7 - active_item_offset_top
    #         
            if self.list_offset > 0:
                self.list_offset = 0
            if self.list_offset < items_on_screen - items_in_list:        
                self.list_offset = items_on_screen - items_in_list
        
        list_offst_px = self.list_offset * item_height
        
        self.clear()
        for idx, item in enumerate(list):
            item_x = 0
            item_y = idx * item_height + list_offst_px
        
            self.display.set_pen(self.palette.primary)
            if item.is_active:
                self.display.rectangle(item_x, item_y, item_width, item_height)
                self.display.set_pen(self.palette.secondary)
            item_label = ('> ' if item.is_selected else '') + item.label
            self.display.text(item_label, item_x + padding, item_y + padding, item_width - 2 * padding, font_scale)
        # ADD SCROLL BAR
        if items_in_list > items_on_screen:
            scroll_width = 18
            scroll_height = self.ui.height
            scroll_x = self.ui.width - scroll_width
            scroll_y = 0
            scroll_padding = 6
            self.display.set_pen(self.palette.secondary)
            self.display.rectangle(scroll_x, scroll_y, scroll_width, scroll_height)
            
            scrollbar_width = scroll_width - scroll_padding * 2
            scrollbar_height = scroll_height - scroll_padding * 2 - scrollbar_width * (items_in_list - items_on_screen)
            scrollbar_x = scroll_x + scroll_padding
            scrollbar_y = scroll_y + scroll_padding + (self.list_offset * -scrollbar_width)
            self.display.set_pen(self.palette.primary)
            self.display.rectangle(scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height)
        self.display.update()
    def get_list_for_render(self):
        return [UIListItem(item, item, self.active_item == idx) for idx, item in enumerate(self.list)]
    def btn_a_handler(self):
        self.activate_prev_item()
    def btn_b_handler(self):
        self.activate_next_item()
    def btn_x_handler(self):
        self.go_back()
    def btn_y_handler(self):
        self.select_item()
    def set_active_item(self, n):
        if len(self.list):
            if n > len(self.list) - 1:
                self.active_item = 0
            elif n < 0:
                self.active_item = len(self.list) - 1
            else:
                self.active_item = n
            self.render()
    def activate_prev_item(self):
        self.set_active_item(self.active_item - 1)
    def activate_next_item(self):
        self.set_active_item(self.active_item + 1)
    def select_item(self, value = None):
        print(f'{self.name}: "{self.list[self.active_item]}" is selected')
        if self.on_select:
            self.on_select(value)
    def go_back(self):
        self.ui.set_active_screen('HOME')
