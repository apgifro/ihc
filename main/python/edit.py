from kivy.app import App
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, SlideTransition
from kivymd.toast import toast
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.menu import MDDropdownMenu

from data.data import open_file, save_to_file


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


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

            toast("Adicionado")

        else:
            for item in data:
                if item[5] == app.item_pos:
                    data[app.item_pos] = [icon, name, price, brand, supplier, app.item_pos]
                    save_to_file(data)
            toast("Editado")

        self.ids.field.icon_right = "shape"
        self.ids.field.text = ""
        self.ids.name.text = ""
        self.ids.price.text = ""
        self.ids.brand.text = ""
        self.ids.supplier.text = ""
        self.ids.toolbar.title = "Adicionar"

        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "start"
        self.manager.transition = SlideTransition(direction="left")

        app.close()
        app.data_update = open_file()
        app.data_original = open_file()
        app.on_start()
