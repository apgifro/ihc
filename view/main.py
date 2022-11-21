from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem


class StartScreen(Screen):
    pass


class AddScreen(Screen):
    pass


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
        for i in range(1, 21):
            start.ids.list.add_widget(
                OneLineListItem(text=f"Produto {i}")
            )

    def back(self):
        self.screen_manager.transition = SlideTransition(direction="right")
        self.screen_manager.current = "start"
        self.screen_manager.transition = SlideTransition(direction="left")


if __name__ == '__main__':
    Estoque().run()
