import os
from screen.list import UIListScreen

class UIFilesScreen(UIListScreen):
    
    def __init__(self, name, ui):
        super().__init__(name, ui)
        self.list: list[str] = self.get_folder_items()
        self.active_item = 0

    def init(self):
        os.chdir('/')
        self.active_item = 0
        super().init()

    def get_folder_items(self) -> list[str]:
        items = []
        for item in os.ilistdir():
            print(item)
            is_folder = item[1] == 0x4000
            prefix = './' if is_folder else ''
            items.append(prefix + item[0])
        items.sort(key=lambda x: (not x.startswith('./'), x))
        return items

    def select_item(self):
        item = self.list[self.active_item]
        if item.startswith('./'):
            os.chdir(item)
            self.list = self.get_folder_items()
            self.active_item = 0
            self.render()

    def go_back(self):
        if os.getcwd() == '/':
            super().go_back()
        else:
            os.chdir('../')
            self.list = self.get_folder_items()
            self.active_item = 0
            self.render()
