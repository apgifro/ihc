from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.list import OneLineListItem, IconLeftWidget, TwoLineIconListItem
from kivymd.uix.textfield import MDTextField

from data.data import open_file, save_to_file
from edit import EditScreen
from splash import SplashScreen


class StartScreen(Screen):
    pass


class Estoque(MDApp):

    def __init__(self):
        super().__init__()
        self.screen_manager = ScreenManager()
        self.data_original = open_file()
        self.data_update = open_file()

    def build(self):
        Builder.load_file("../src/layouts/splash.kv")
        Builder.load_file("../src/layouts/start.kv")
        Builder.load_file("../src/layouts/edit.kv")

        self.screen_manager.add_widget(SplashScreen(name="splash"))
        self.screen_manager.add_widget(StartScreen(name='start'))
        self.screen_manager.add_widget(EditScreen(name='edit'))
        self.screen_manager.current = "splash"

        return self.screen_manager

    def on_start(self):
        start = self.screen_manager.get_screen("start")
        start.ids.list.clear_widgets()

        if self.data_update:
            for x in range(len(self.data_update)):
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
                OneLineListItem(text=f"Clique no + para adicionar o primeiro produto"),
            )

    def click(self, value):
        self.item_pos = int(value.id)
        self.screen_manager.current = "edit"
        edit = self.screen_manager.get_screen("edit")
        edit.ids.toolbar.title = "Editar"

        icon = self.data_update[self.item_pos][0]

        if icon == "home":
            icon_name = "Casa"
        elif icon == "glass-cocktail":
            icon_name = "Alimento e Bebida"
        elif icon == "tshirt-crew":
            icon_name = "Roupas"
        elif icon == "cellphone":
            icon_name = "Eletrônicos"
        else:
            icon_name = "Outros"

        edit.ids.field.text = icon_name

        edit.ids.field.icon_right = self.data_update[self.item_pos][0]
        edit.ids.name.text = self.data_update[self.item_pos][1]
        edit.ids.price.text = self.data_update[self.item_pos][2]
        edit.ids.brand.text = self.data_update[self.item_pos][3]
        edit.ids.supplier.text = self.data_update[self.item_pos][4]

        edit.ids.box_delete.add_widget(
            MDRaisedButton(
                text="Excluir",
                pos_hint={"left": 1},
                size_hint=(0.2, 0),
                on_release=self.remove,
                md_bg_color="red"
            )
        )

    def remove(self, button):
        screen = self.screen_manager.current
        del self.data_original[self.item_pos]
        save_to_file(self.data_original)

        toast("Excluído")

        self.back()

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
            self.data_update.append(["magnify",
                                     "Nenhum resultado encontrado",
                                     "Tente usar palavras-chave diferentes"])

        self.on_start()

    def close(self):

        start = self.screen_manager.get_screen("start")
        toolbar = start.ids.toolbar
        toolbar.left_action_items = []
        toolbar.title = "Estoque"
        toolbar.right_action_items = [["magnify", lambda x: self.search()]]

        try:
            edit = self.screen_manager.get_screen("edit")
            edit.ids.box_delete.clear_widgets()
        except:
            pass

        self.data_original = open_file()
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
            edit.ids.field.text = ""
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
