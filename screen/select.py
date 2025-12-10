from screen.list import UIListScreen, UIListItem

class UISelectScreen(UIListScreen):
    """Selection list screen with current value indication."""
    
    def __init__(self, name, ui, items_list, value, on_select):
        super().__init__(name, ui, on_select)
        self.list = items_list
        self.value = value
    def get_list_for_render(self):
        return [UIListItem(
            item[0],
            item[1],
            self.active_item == idx,
            item[1] == self.value) for idx, item in enumerate(self.list)
        ]
    def select_item(self):
        value = self.list[self.active_item][1]
        self.value = value
        super().select_item(value)
        self.render()
    def go_back(self):
        self.ui.set_active_screen('SETTINGS')