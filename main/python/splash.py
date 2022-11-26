from kivy.clock import Clock
from kivy.uix.screenmanager import Screen


class SplashScreen(Screen):

    def on_enter(self, *args):

        Clock.schedule_once(self.switch_to_home, 1)

    def switch_to_home(self, x):
        # self.manager.transition = FadeTransition()
        self.manager.current = 'start'