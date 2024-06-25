from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import SlideTransition
from kivy.clock import Clock
from kivy.storage.jsonstore import JsonStore
import random
import time
import difflib
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivy.animation import Animation
from kivy_garden.graph import Graph, MeshLinePlot
from screens import WelcomeScreen, MainScreen, HistoryScreen, GraphScreen

class TypingSpeedApp(MDApp):
    def build(self):
        self.texts = [
            "In a poor world, poor matters",
            "Miserable life and fun",
            "There are daily quarrels",
            "There is no day without a fierce pipe",
            "Father runs barefoot",
            "There is a brawl and a fight",
            "No one explains to anyone",
            "To try to live differently",
            "Pa pa pa pa pa pa",
            "This is exactly the Kiepski world",
            "Pa pa pa pa pa pa",
            "Kiepski life Kiepski world",
            "There are hopes and loves",
            "There are victories and joys",
            "There are scandals and noises",
            "Gyrations on the couch",
            "Although the problems are cosmic",
            "It's quite nice here",
            "This is exactly Kiepski's life",
            "You will see, you will believe"
        ]
        self.speed = 0
        self.accuracy = 0
        self.time_start = 0
        self.time_end = 0
        self.timer_event = None

        # Set default theme
        self.current_theme = "Dark"
        self.set_theme(self.current_theme)

        self.store = JsonStore('typing_speed_history.json')

        screen_manager = Builder.load_file('kv_strings.kv')
        screen_manager.transition = SlideTransition(duration=0.5)

        # Adding Footer
        main_screen = screen_manager.get_screen('main')
        footer = BoxLayout(orientation='horizontal', padding=5, size_hint_y=None, height='40dp')
        footer.add_widget(MDLabel(text="Code created by Tymoteusz Maja, GitHub: Xeraoo", halign="center", theme_text_color="Secondary"))
        main_screen.add_widget(footer)

        return screen_manager

    def start(self):
        self.time_start = time.time()
        self.root.get_screen('main').ids.user_text.text = ""
        self.root.get_screen('main').ids.label_timer.text = "Time: 0.0 s"
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 0.1)

    def stop(self):
        self.time_end = time.time()
        elapsed_time = self.time_end - self.time_start
        words = self.root.get_screen('main').ids.label_text.text.split(' ')
        self.speed = round(len(words) / (elapsed_time / 60))
        self.accuracy = round(difflib.SequenceMatcher(None, self.root.get_screen('main').ids.label_text.text, self.root.get_screen('main').ids.user_text.text).ratio() * 100)
        self.root.get_screen('main').ids.label_speed.text = f"Your typing speed is {self.speed} WPM"
        self.root.get_screen('main').ids.label_accuracy.text = f"Your typing accuracy is {self.accuracy} %"
        if self.timer_event:
            self.timer_event.cancel()

        self.save_result(elapsed_time)

    def new_text(self):
        self.root.get_screen('main').ids.label_text.text = random.choice(self.texts)

    def set_theme(self, theme):
        self.current_theme = theme
        if theme == "Light":
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Orange"

    def update_timer(self, dt):
        elapsed_time = time.time() - self.time_start
        self.root.get_screen('main').ids.label_timer.text = f"Time: {elapsed_time:.1f} s"

    def animate_button(self, button):
        anim = Animation(size=(220, 55), duration=0.1) + Animation(size=(200, 50), duration=0.1)
        anim.start(button)

    def go_to_main(self):
        self.animate_button(self.root.get_screen('welcome').ids.start_button)
        self.root.current = 'main'

    def go_to_history(self):
        self.root.current = 'history'
        self.update_history_list()

    def go_to_graph(self):
        self.root.current = 'graph'
        self.update_graph()

    def update_history_list(self):
        history_list = self.root.get_screen('history').ids.history_list
        history_list.clear_widgets()

        for key in sorted(self.store.keys(), reverse=True):
            result = self.store.get(key)
            date = key
            speed = result['speed']
            accuracy = result['accuracy']
            history_item = MDLabel(text=f"{date} - Speed: {speed} WPM, Accuracy: {accuracy} %", halign="center", size_hint_y=None, height='40dp')
            history_list.add_widget(history_item)

    def save_result(self, elapsed_time):
        result = {
            'time': elapsed_time,
            'speed': self.speed,
            'accuracy': self.accuracy
        }
        self.store.put(str(time.time()), **result)

    def update_graph(self):
        graph_container = self.root.get_screen('graph').ids.graph_container
        graph_container.clear_widgets()

        speed_values = []
        accuracy_values = []

        for key in sorted(self.store.keys(), reverse=True):
            result = self.store.get(key)
            speed = result['speed']
            accuracy = result['accuracy']
            speed_values.append(speed)
            accuracy_values.append(accuracy)

        # Create a graph
        graph = Graph(
            xlabel='Attempt',
            ylabel='WPM / Accuracy',
            x_ticks_minor=1,
            x_ticks_major=1,
            y_ticks_major=10,
            y_grid_label=True,
            x_grid_label=True,
            padding=5,
            xlog=False,
            ylog=False,
            x_grid=True,
            y_grid=True,
            xmin=-0.5,
            xmax=len(speed_values) - 0.5,
            ymin=min(min(speed_values), min(accuracy_values)) - 10,
            ymax=max(max(speed_values), max(accuracy_values)) + 10,
            size_hint_y=None,
            height='400dp'
        )

        plot_speed = MeshLinePlot(color=[1, 0, 0, 1])
        plot_speed.points = [(i, speed) for i, speed in enumerate(speed_values)]
        graph.add_plot(plot_speed)

        plot_accuracy = MeshLinePlot(color=[0, 1, 0, 1])
        plot_accuracy.points = [(i, accuracy) for i, accuracy in enumerate(accuracy_values)]
        graph.add_plot(plot_accuracy)

        graph_container.add_widget(graph)

if __name__ == "__main__":
    TypingSpeedApp().run()
