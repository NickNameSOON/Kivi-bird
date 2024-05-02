from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
import random

class ClickerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_count = 0
        self.bird_y = Window.height / 2
        self.bird_velocity = 0
        self.game_over = False
        self.started = False
        self.gap_size = 150  # Gap size between the pipes

    def build(self):
        self.root = FloatLayout()

        # Background image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.root.add_widget(background)

        # Score label
        self.label = Label(text='Score: 0', size_hint=(1, None), height=50, pos_hint={'top': 1})
        self.root.add_widget(self.label)

        # Bird image
        self.bird_image = Image(source='bird.png', size_hint=(None, None), size=(100, 100), pos_hint={'center_x': 0.2, 'center_y': 0.5})
        self.root.add_widget(self.bird_image)

        # Pipes
        self.bar1 = Image(source='tube.png', size_hint=(None, None), size=(50, 300), pos_hint={'right': 1, 'top': 1})
        self.root.add_widget(self.bar1)
        self.bar2 = Image(source='tube2.png', size_hint=(None, None), size=(50, 300), pos_hint={'right': 1, 'y': 0})
        self.root.add_widget(self.bar2)

        # Buttons
        btn_layout = BoxLayout(size_hint=(1, None), height=50, pos_hint={'y': 0})
        self.start_button = Button(text='Start Game')
        self.start_button.bind(on_press=self.start_game)
        btn_layout.add_widget(self.start_button)

        self.reset_button = Button(text='Restart Game', disabled=True)
        self.reset_button.bind(on_press=self.restart_game)
        btn_layout.add_widget(self.reset_button)

        self.up_button = Button(text='Fly Up', disabled=True)
        self.up_button.bind(on_press=self.fly_up)
        btn_layout.add_widget(self.up_button)

        self.root.add_widget(btn_layout)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return self.root

    def start_game(self, instance):
        self.start_button.disabled = True
        self.reset_button.disabled = False
        self.up_button.disabled = False
        self.game_over = False
        self.started = False
        self.score_count = 0
        self.bird_y = Window.height / 2
        self.label.text = 'Score: 0'
        self.bird_image.pos_hint = {'center_x': 0.2, 'center_y': self.bird_y / Window.height}
        self.bar1.x = self.bar1.x - 3  # Update bar1.x with the new position
        self.bar2.x = self.bar2.x - 3  # Update bar2.x with the new position


    def restart_game(self, instance):
        self.start_game(instance)

    def fly_up(self, instance):
        if not self.game_over:
            if not self.started:
                self.started = True
            self.bird_velocity = 10

    def update(self, dt):
        if not self.game_over and self.started:
            self.bird_velocity -= 0.5
            self.bird_y += self.bird_velocity
            self.bird_image.pos_hint = {'center_x': 0.2, 'center_y': self.bird_y / Window.height}

            if self.bird_y < 0 or self.bird_y + self.bird_image.height > Window.height:
                self.game_over = True
                self.label.text = 'Game Over!'
                self.up_button.disabled = True  # Disable the button on game over

            self.bar1.x -= 3
            self.bar2.x -= 3

            # Reset pipes and randomize gap position
            if self.bar1.right <= 0:
                self.bar1.x = Window.width
                self.bar2.x = Window.width
                new_gap = random.randint(100, Window.height - 400)  # Randomize the vertical position of the gap
                self.bar1.top = Window.height - new_gap
                self.bar2.y = self.bar1.top - self.gap_size
                self.score_count += 1
                self.label.text = f'Score: {self.score_count}'

            if (self.bird_image.collide_widget(self.bar1) or self.bird_image.collide_widget(self.bar2)):
                self.game_over = True
                self.label.text = 'Game Over!'
                self.up_button.disabled = True  # Disable the button on game over

if __name__ == '__main__':
    ClickerApp().run()
