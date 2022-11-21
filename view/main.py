from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, TwoLineListItem
from data.data import open_file, save_to_file


class StartScreen(Screen):
    pass


class AddScreen(Screen):

    def get(self):
        name = self.ids.name.text
        price = self.ids.price.text
        brand = self.ids.brand.text
        supplier = self.ids.supplier.text
        data = open_file()
        if data:
            data_to_save = data + [[name, price, brand, supplier]]
            save_to_file(data_to_save)
        else:
            data_to_save = [[name, price, brand, supplier]]
            save_to_file(data_to_save)


class Estoque(MDApp):

    def build(self):
        Builder.load_file("screens.kv")

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(StartScreen(name='start'))
        self.screen_manager.add_widget(AddScreen(name='add'))
        self.screen_manager.current = "start"

        return self.screen_manager

    def on_start(self):
        start = self.screen_manager.get_screen("start")
        start.ids.list.clear_widgets()
        data = open_file()
        if data:
            print(data)
            for x in range(len(data)):
                start.ids.list.add_widget(
                    TwoLineListItem(text=f"{data[x][0]}",
                                    secondary_text=f"{data[x][2]}",
                                    )
                )
        else:
            start.ids.list.add_widget(
                OneLineListItem(text=f"Clique no + para adicionar o primeiro produto."),
            )

    def back(self):
        self.screen_manager.transition = SlideTransition(direction="right")
        self.screen_manager.current = "start"
        self.screen_manager.transition = SlideTransition(direction="left")
        self.on_start()


if __name__ == '__main__':
    Estoque().run()
