from screen.list import UIListScreen, UIListItem

class UISettingsScreen(UIListScreen):
    """Settings menu screen."""
    
    def __init__(self, name, ui, items_list, on_select):
        super().__init__(name, ui, on_select)
        self.list = items_list
    def get_list_for_render(self):
        return [UIListItem(item[0], item[1], self.active_item == idx) for idx, item in enumerate(self.list)]
    def select_item(self):
        value = self.list[self.active_item][1]
        super().select_item(value)