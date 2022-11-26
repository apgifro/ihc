from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem, IconLeftWidget, TwoLineIconListItem, OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField

from data.data import open_file, save_to_file


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class StartScreen(Screen):
    pass


class EditScreen(Screen):

    def open(self):

        app = App.get_running_app()
        self.screen = app.screen_manager.get_screen("edit")

        menu_items = [
            {
                "viewclass": "IconListItem",
                "icon": "home",
                "height": dp(56),
                "text": f"Casa",
                "on_release": lambda x=f"Item i": self.set_item("Casa", "home"),
            },

            {
                "viewclass": "IconListItem",
                "icon": "glass-cocktail",
                "height": dp(56),
                "text": f"Alimento e Bebida",
                "on_release": lambda x=f"Item i": self.set_item("Alimento e Bebida", "glass-cocktail"),
            },

            {
                "viewclass": "IconListItem",
                "icon": "tshirt-crew",
                "height": dp(56),
                "text": f"Roupas",
                "on_release": lambda x=f"Item i": self.set_item("Roupas", "tshirt-crew"),
            },

            {"viewclass": "IconListItem",
             "icon": "cellphone",
             "height": dp(56),
             "text": f"Eletrônicos",
             "on_release": lambda x=f"Item i": self.set_item("Eletrônicos", "cellphone")},

            {"viewclass": "IconListItem",
             "icon": "shape",
             "height": dp(56),
             "text": f"Outro",
             "on_release": lambda x=f"Item i": self.set_item("Outro", "shape")}
        ]

        self.menu = MDDropdownMenu(
            caller=self.screen.ids.field,
            items=menu_items,
            position="bottom",
            width_mult=8,
        )

        self.menu.open()

    def menu_callback(self, text_item):
        print(text_item)

    def set_item(self, text__item, icon):
        self.screen.ids.field.text = text__item
        self.screen.ids.field.icon_right = icon
        self.menu.dismiss()

    def get(self):

        app = App.get_running_app()

        icon = self.ids.field.icon_right
        name = self.ids.name.text
        price = self.ids.price.text
        brand = self.ids.brand.text
        supplier = self.ids.supplier.text

        data = open_file()
        id = 0
        if data:
            id = len(data)

        if self.ids.toolbar.title == "Adicionar":

            if data:
                data_to_save = data + [[icon, name, price, brand, supplier, id]]
                save_to_file(data_to_save)
            else:
                data_to_save = [[icon, name, price, brand, supplier, id]]
                save_to_file(data_to_save)

        else:
            for item in data:
                print(item)
                if item[5] == app.item_pos:
                    data[app.item_pos] = [icon, name, price, brand, supplier, app.item_pos]
                    save_to_file(data)

        self.ids.field.icon_right = "shape"
        self.ids.name.text = ""
        self.ids.price.text = ""
        self.ids.brand.text = ""
        self.ids.supplier.text = ""

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "start"
        self.manager.transition = SlideTransition(direction="left")

        app.close()
        app.data_update = open_file()
        app.data_original = open_file()
        app.on_start()


class Estoque(MDApp):

    def build(self):
        Builder.load_file("view/start.kv")
        Builder.load_file("view/edit.kv")

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(StartScreen(name='start'))
        self.screen_manager.add_widget(EditScreen(name='edit'))
        self.screen_manager.current = "start"

        self.data_original = open_file()
        self.data_update = open_file()

        return self.screen_manager

    def on_start(self):
        start = self.screen_manager.get_screen("start")
        start.ids.list.clear_widgets()

        if self.data_update:
            print("/////////")
            for x in range(len(self.data_update)):
                print(self.data_update[x])
                start.ids.list.add_widget(
                    TwoLineIconListItem(IconLeftWidget(
                        icon=self.data_update[x][0]
                    ),
                        id=str(x),
                        text=f"{self.data_update[x][1]}",
                        secondary_text=f"{self.data_update[x][2]}",
                        on_release=self.click
                    )
                )
        else:
            start.ids.list.add_widget(
                OneLineListItem(text=f"Clique no + para adicionar o primeiro produto."),
            )

    def click(self, value):
        self.item_pos = int(value.id)
        self.screen_manager.current = "edit"
        edit = self.screen_manager.get_screen("edit")
        edit.ids.toolbar.title = "Editar"

        icon = self.data_original[self.item_pos][0]
        icon_name = "Outro"
        if icon == "home":
            icon_name = "Casa"
        elif icon == "glass-cocktail":
            icon_name = "Alimento e Bebida"
        elif icon == "tshirt-crew":
            icon_name = "Roupas"
        else:
            icon_name = "Eletrônicos"

        edit.ids.field.text = icon_name

        edit.ids.field.icon_right = self.data_original[self.item_pos][0]
        edit.ids.name.text = self.data_original[self.item_pos][1]
        edit.ids.price.text = self.data_original[self.item_pos][2]
        edit.ids.brand.text = self.data_original[self.item_pos][3]
        edit.ids.supplier.text = self.data_original[self.item_pos][4]

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
                if text in item[1].lower():
                    self.data_update.append(item)

        if len(self.data_update) == 0:
            self.data_update.append(["magnify", "Nenhum resultado encontrado...", "Tente usar palavras-chave diferentes"])

        self.on_start()

    def close(self):
        start = self.screen_manager.get_screen("start")
        toolbar = start.ids.toolbar
        toolbar.left_action_items = []
        toolbar.title = "Estoque"
        toolbar.right_action_items = [["magnify", lambda x: self.search()]]
        self.data_update = self.data_original[:]
        try:
            start.remove_widget(self.search_input)
        except:
            pass
        self.on_start()

    def back(self):
        self.screen_manager.transition = SlideTransition(direction="right")
        self.screen_manager.current = "start"
        self.screen_manager.transition = SlideTransition(direction="left")

        try:
            edit = self.screen_manager.get_screen("edit")
            edit.ids.field.icon_right = "shape"
            edit.ids.name.text = ""
            edit.ids.price.text = ""
            edit.ids.brand.text = ""
            edit.ids.supplier.text = ""
            edit.ids.toolbar.title = "Adicionar"
        except:
            pass

        self.close()
        self.on_start()


if __name__ == '__main__':
    Estoque().run()
