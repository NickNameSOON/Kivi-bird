from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock


class ClickerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score_count = 0
        self.bird_y = 300
        self.bird_velocity = 0
        self.game_over = False

    def build(self):
        self.root = FloatLayout()

        # Background image
        background = Image(source='background.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
        self.root.add_widget(background)

        layout = BoxLayout(orientation='vertical', padding=10)
        # Window.size = (800, 600)

        self.label = Label(text='Clicks: 0', size_hint=(1, 0.1))
        layout.add_widget(self.label)

        # BoxLayout для розташування стовпців один над одним
        bars_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6))
        layout.add_widget(bars_layout)

        # Перший стовпець (зверху)
        self.bar1 = Image(source='tub.png', size_hint=(None, None), size=(50, 300))
        bars_layout.add_widget(self.bar1)

        # Проміжок, через який може пролетіти птах
        self.gap = Image(source='space.png', size_hint=(None, None), size=(75, 200))
        bars_layout.add_widget(self.gap)

        # Другий стовпець (знизу)
        self.bar2 = Image(source='tub.png', size_hint=(None, None), size=(50, 300))
        bars_layout.add_widget(self.bar2)

        # Кнопки та інші віджети
        self.bird_image = Image(source='bird.png', size_hint=(None, None), size=(100, 100))
        layout.add_widget(self.bird_image)

        self.start_button = Button(text='Start Game', size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start_game)
        layout.add_widget(self.start_button)

        self.reset_button = Button(text='Restart Game', size_hint=(1, 0.1))
        self.reset_button.bind(on_press=self.restart_game)
        self.reset_button.disabled = True
        layout.add_widget(self.reset_button)

        self.up_button = Button(text='Fly Up', size_hint=(1, 0.1))
        self.up_button.bind(on_press=self.fly_up)
        layout.add_widget(self.up_button)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

        return layout

    def start_game(self, instance):
        self.start_button.disabled = True
        self.reset_button.disabled = False
        self.up_button.disabled = False
        self.score_count = 0
        self.bird_y = Window.height / 2
        self.bird_velocity = 0
        self.game_over = False
        self.label.text = 'Score: 0'

        # Рухаємо стовпи за межі екрану
        self.bar1.x = Window.width
        self.bar2.x = Window.width

    def restart_game(self, instance):
        self.start_game(instance)

    def fly_up(self, instance):
        if not self.game_over:
            self.bird_velocity = 5

    def on_key_up(self, window, key, *args):
        if key == 32:
            self.bird_velocity = -5

    def update(self, dt):
        if not self.game_over:
            self.bird_velocity -= 0.2  # Add gravity
            self.bird_y += self.bird_velocity

            # Prevent bird from going out of window
            if self.bird_y < 0:
                self.bird_y = 0
                self.game_over = True
                self.label.text = 'Game Over!'
            elif self.bird_y > Window.height - self.bird_image.height:
                self.bird_y = Window.height - self.bird_image.height
                self.game_over = True
                self.label.text = 'Game Over!'

            self.bird_image.y = self.bird_y

            # Update position of bars and gap
            self.bar1.x -= 5
            self.bar2.x -= 5

            # Dynamically adjust gap position based on bar positions
            self.gap.x = self.bar1.x + (self.bar2.x - self.bar1.x) / 2 - self.gap.width / 2

            if self.bar1.x <= -self.bar1.width:
                self.bar1.x = Window.width
                self.bar2.x = Window.width
                self.score_count += 1
                self.label.text = f'Score: {self.score_count}'

            # Check collision with gap instead of bars
            if (self.bird_image.x < self.gap.x + self.gap.width and
                    self.bird_image.x + self.bird_image.width > self.gap.x and
                    (self.bird_image.y < self.gap.y or
                     self.bird_image.y + self.bird_image.height > self.gap.y + self.gap.height)):
                self.game_over = True
                self.label.text = 'Game Over!'


if __name__ == '__main__':
    ClickerApp().run()
