from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem, TwoLineListItem
from kivymd.uix.textfield import MDTextField

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

        self.ids.name.text = ""
        self.ids.price.text = ""
        self.ids.brand.text = ""
        self.ids.supplier.text = ""

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "start"
        self.manager.transition = SlideTransition(direction="left")

        app = App.get_running_app()
        app.on_start()


class Estoque(MDApp):

    def build(self):
        Builder.load_file("view/start.kv")
        Builder.load_file("view/add.kv")

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(StartScreen(name='start'))
        self.screen_manager.add_widget(AddScreen(name='add'))
        self.screen_manager.current = "start"

        self.data_original = open_file()
        self.data_update = self.data_original[:]

        return self.screen_manager

    def on_start(self):
        start = self.screen_manager.get_screen("start")
        start.ids.list.clear_widgets()
        if self.data_update:
            for x in range(len(self.data_update)):
                start.ids.list.add_widget(
                    TwoLineListItem(text=f"{self.data_update[x][0]}",
                                    secondary_text=f"{self.data_update[x][1]}",
                                    )
                )
        else:
            start.ids.list.add_widget(
                OneLineListItem(text=f"Clique no + para adicionar o primeiro produto."),
            )

    def search(self):

        start = self.screen_manager.get_screen("start")

        self.search_input = (
            MDFloatLayout(
                MDTextField(
                    pos_hint={"center_x": 0.5, "top": True},
                    size_hint=(0.8, 0.1),
                    line_color_focus=(1, 1, 1, 1),
                    line_color_normal=(1, 1, 1, 1),
                    text_color_normal=(1, 1, 1, 1),
                    text_color_focus=(1, 1, 1, 1),
                    on_text_validate=self.search_text,
                ),
                id="input_search"
            )
        )
        start.add_widget(self.search_input)

        toolbar = start.ids.toolbar
        toolbar.title = ""
        toolbar.right_action_items = [["keyboard-return"]]
        toolbar.left_action_items = [["arrow-left", lambda x: self.close()]]

    def search_text(self, value):
        text = value.text.lower()

        data = self.data_original[:]
        self.data_update = []
        if data:
            for item in data:
                if text in item[0].lower():
                    self.data_update.append(item)

        if len(self.data_update) == 0:
            self.data_update.append(["Sem resultados...", "Faça uma nova busca"])

        self.on_start()

    def close(self):
        start = self.screen_manager.get_screen("start")
        toolbar = start.ids.toolbar
        toolbar.left_action_items = []
        toolbar.title = "Estoque"
        toolbar.right_action_items = [["magnify", lambda x: self.search()]]
        print(self.data_original)
        print(self.data_update)
        self.data_update = self.data_original[:]
        print(self.data_update)
        try:
            start.remove_widget(self.search_input)
        except:
            pass
        self.on_start()


    def back(self):
        self.screen_manager.transition = SlideTransition(direction="right")
        self.screen_manager.current = "start"
        self.screen_manager.transition = SlideTransition(direction="left")
        self.close()
        self.on_start()


if __name__ == '__main__':
    Estoque().run()
