from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.clock import Clock
import most_common_words


class TypingSpeedTest(App):
    def __init__(self):
        super(TypingSpeedTest, self).__init__()
        self.text_list = []
        self.current_word_index = 0
        self.text = ''
        self.user_text_list = []
        self.user_text = ''
        self.start = False
        self.clock = Clock
        self.time = 60

    def build(self):
        self.main_window = BoxLayout(orientation="vertical", padding=5)
        self.main_window_label = Label(text="Typing Speed Test", font_family='Sans', font_size=50, size_hint=(1, .3), pos_hint={"center_x": 0.5, "center_y": .5})
        self.top_window = BoxLayout(orientation="horizontal",)
        self.top_window_text = TextInput(multiline=True, readonly=True, size_hint=(.8, 1), padding=8)
        self.top_window_options = BoxLayout(orientation="vertical", size_hint=(.2, 1))
        self.top_window_options_timer = TextInput(text="60", readonly=True, multiline=False, background_color="gray", font_size=40, halign="center", size_hint=(.9, .2), pos_hint={"center_x": 0.5, "center_y": .5})
        self.top_window_options_newtext = Button(text="", disabled=True, size_hint=(.9, .7), pos_hint={"center_x": 0.5, "top": 0})
        self.top_window_options_newtext.bind(on_press=self.add_text)
        self.top_window_options.add_widget(self.top_window_options_timer)
        self.top_window_options.add_widget(self.top_window_options_newtext)

        self.top_window.add_widget(self.top_window_text)
        self.top_window.add_widget(self.top_window_options)

        self.bottom_window = BoxLayout(orientation="horizontal",)
        self.bottom_window_text = TextInput(multiline=True, size_hint=(.8, 1), padding=8)

        Window.bind(on_key_down=self.compare)

        self.bottom_window_options = BoxLayout(orientation="vertical", size_hint=(.2, 1))
        self.bottom_window_options_wpm_label = Label(text="Total Words:", color="lightgray", size_hint=(.9, .1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.bottom_window_options_wpm = Button(text="0", background_color="lightgray", size_hint=(.9, .1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.bottom_window_options_accuracy_label = Label(text="Accuracy:", color="lightblue", size_hint=(.9, .1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.bottom_window_options_accuracy = Button(text="100 %", background_color="lightblue", size_hint=(.9, .1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.bottom_window_options_reset = Button(text="Reset", background_color="green", size_hint=(.9, .3), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.bottom_window_options_reset.bind(on_press=self.reset)

        self.bottom_window_options.add_widget(self.bottom_window_options_wpm_label)
        self.bottom_window_options.add_widget(self.bottom_window_options_wpm)
        self.bottom_window_options.add_widget(self.bottom_window_options_accuracy_label)
        self.bottom_window_options.add_widget(self.bottom_window_options_accuracy)
        self.bottom_window_options.add_widget(self.bottom_window_options_reset)

        self.bottom_window.add_widget(self.bottom_window_text)
        self.bottom_window.add_widget(self.bottom_window_options)

        self.main_window.add_widget(self.main_window_label)
        self.main_window.add_widget(self.top_window)
        self.main_window.add_widget(self.bottom_window)

        self.add_text()


        return self.main_window

    def add_text(self, *args, **kwargs):
        self.text_list = most_common_words.random_string()
        self.display_text()

    def compare(self, *args):
        if self.bottom_window_text.focus:

            if not self.start and not self.user_text_list:
                self.start_timer()
                self.start = True

            self.highlight()
            keycode = args[1]

            # when user hits spacebar - Check last word against database last word
            if keycode == 32:
                self.user_text = self.bottom_window_text.text
                self.user_text_list = self.user_text.split(" ")
                user_last_word = self.user_text_list[-1]
                self.current_word_index = len(self.user_text_list)

    def highlight(self):
        current = self.text_list[self.current_word_index]
        start_index = self.text.find(current)
        end_index = start_index + len(current)
        self.top_window_text.select_text(start_index, end_index)

    def display_text(self):
        self.text = " ".join(self.text_list)
        self.top_window_text.text = self.text

    def start_timer(self):
        self.clock = Clock.schedule_interval(self.run_timer, 1)

    def run_timer(self, *args, **kwargs):
        time_output = str(self.time)
        if self.time >= 0:
            self.time -= 1
            self.display_results()
            self.top_window_options_timer.text = time_output
        if self.time > 10:
            self.top_window_options_timer.background_color = 'green'
        if 10 > self.time > 0:
            self.top_window_options_timer.background_color = 'yellow'

        if self.time == 0:
            self.top_window_options_timer.background_color = 'red'
            self.clock.cancel()
            self.time = 60
            self.start = False
            self.top_window_options_timer.text = f"STOP"




    def reset(self, *args, **kwargs):
        self.time = 60
        self.start = False
        self.user_text_list = []
        self.user_text = ""
        self.top_window_options_timer.text = str(self.time)
        self.top_window_text.select_text(0, 0)
        self.top_window_text.background_color = "white"
        self.top_window_options_timer.background_color = 'gray'
        self.bottom_window_text.text = self.user_text
        self.bottom_window_options_accuracy.text = '100 %'

        # if self.clock is still BASE CLOCK no cancel function is necessary. This avoids error.
        if self.clock != Clock:
            self.clock.cancel()
        self.add_text()

    def display_results(self):
        user_list_length = len(self.user_text_list)
        total_correct = int(user_list_length)
        for x, y in zip(self.user_text_list, self.text_list[:user_list_length]):
            if x != y:
                total_correct -= 1

        self.bottom_window_options_wpm.text = f"{total_correct}"

        if user_list_length:
            accuracy = (total_correct / user_list_length) * 100
            self.bottom_window_options_accuracy.text = "{:.2f} %".format(accuracy)


if __name__ == "__main__":
    app = TypingSpeedTest()
    app.run()

