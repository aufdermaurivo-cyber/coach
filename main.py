import time
import random
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

class FloatingPornButton(Button):
    def __init__(self, callback_func, **kwargs):
        super().__init__(**kwargs)
        self.text = "PORN / PAUSE"
        self.bold = True
        self.font_size = '18sp'
        self.background_color = (1, 0, 0, 0.9)
        self.size_hint = (None, None)
        self.size = (180, 80)
        self.pos = (Window.width - 200, 100)
        self.callback_func = callback_func

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab is self:
            self.center_x = touch.x
            self.center_y = touch.y
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab is self:
            touch.ungrab(self)
            self.callback_func()
            return True
        return super().on_touch_up(touch)

class StaminaAICoach(App):
    def build(self):
        self.title = "Stamina AI Coach Pro"
        self.is_session_active = False
        self.is_porn_mode = False
        self.current_hr = 110
        self.previous_hr = 110
        self.current_hrv = 65
        self.target_hr_max = 145
        self.target_hr_min = 120
        self.wave_step = 0

        self.root_layout = FloatLayout()
        scroll = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        self.label_status = Label(text="Bereit für Training", font_size='22sp', size_hint_y=None, height=40)
        content.add_widget(self.label_status)

        self.label_hr = Label(text="Puls: -- bpm | HRV: -- ms", font_size='24sp', bold=True, size_hint_y=None, height=50)
        content.add_widget(self.label_hr)

        self.label_toy_status = Label(text="Arcwave: Hub 0% | Rot 0% || Diamo: 0%", font_size='15sp', size_hint_y=None, height=35)
        content.add_widget(self.label_toy_status)

        self.btn_start = Button(text="Session Starten", background_color=(0, 0.8, 0, 1), font_size='20sp', size_hint_y=None, height=60)
        self.btn_start.bind(on_press=self.toggle_session)
        content.add_widget(self.btn_start)

        self.label_ai = Label(text="KI Coaching: Sensoren bereit", font_size='14sp', size_hint_y=None, height=100)
        content.add_widget(self.label_ai)

        scroll.add_widget(content)
        self.root_layout.add_widget(scroll)

        self.porn_btn = FloatingPornButton(callback_func=self.trigger_porn_button)
        return self.root_layout

    def toggle_session(self, instance):
        if not self.is_session_active:
            self.is_session_active = True
            self.is_porn_mode = False
            self.btn_start.text = "Session Beenden"
            self.btn_start.background_color = (0.8, 0.5, 0, 1)
            self.label_status.text = "Session Aktiv"
            if self.porn_btn not in self.root_layout.children:
                self.root_layout.add_widget(self.porn_btn)
            Clock.schedule_interval(self.process_loop, 2.0)
        else:
            self.end_session()

    def process_loop(self, dt):
        if not self.is_session_active:
            return False

        self.previous_hr = self.current_hr
        self.current_hr = random.randint(118, 148)
        self.current_hrv = random.randint(40, 70)
        self.label_hr.text = f"Puls: {self.current_hr} bpm | HRV: {self.current_hrv} ms"

        if (self.current_hr - self.previous_hr >= 8 or self.current_hrv < 30) and not self.is_porn_mode:
            self.is_porn_mode = True
            self.label_status.text = "AUTO-SAFETY: Steiler Pulsanstieg erkannt!"

        if self.is_porn_mode:
            self.label_toy_status.text = "PORN-MODUS: Arcwave STOPP (0%) | Diamo 15%"
            if self.current_hr <= self.target_hr_min:
                self.is_porn_mode = False
                self.label_status.text = "Puls erholt – Training läuft weiter"
        else:
            if self.current_hr > self.target_hr_max:
                self.label_toy_status.text = "KI: Hub gedrosselt (20%), Rotation Stopp"
            elif self.current_hr < self.target_hr_min:
                self.label_toy_status.text = "KI: Hub 70%, Rotation 50%"
            else:
                self.wave_step = (self.wave_step + 1) % 4
                self.label_toy_status.text = f"KI: Bio-Waveing Rhythmus {self.wave_step + 1}"

    def trigger_porn_button(self):
        if self.is_session_active:
            self.is_porn_mode = True
            self.label_status.text = "PORN BUTTON AKTIVIERT"

    def end_session(self):
        self.is_session_active = False
        Clock.unschedule(self.process_loop)
        if self.porn_btn in self.root_layout.children:
            self.root_layout.remove_widget(self.porn_btn)
        self.btn_start.text = "Session Starten"
        self.btn_start.background_color = (0, 0.8, 0, 1)
        self.label_status.text = "Session Beendet"

if __name__ == '__main__':
    StaminaAICoach().run()
