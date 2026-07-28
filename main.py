# main.py
from kivy.app import App
from kivy.properties import NumericProperty
from kivy.lang import Builder

# Загружаем KV-разметку прямо из строки, чтобы не было проблем с именами файлов
KV_CODE = """
<MainLayout>:
    orientation: 'vertical'
    padding: 20
    spacing: 15
    
    # Фон
    canvas.before:
        Color:
            rgba: 0.05, 0, 0.15, 1  # Тёмно-фиолетовый
        Rectangle:
            pos: self.pos
            size: self.size
    
    # Заголовок
    Label:
        text: '✨ Y2K CLICKER ✨'
        font_size: '36sp'
        color: 1, 0, 1, 1  # Неон-розовый
        size_hint_y: 0.2
    
    # Счёт
    Label:
        text: f'Очки: {app.score}'
        font_size: '48sp'
        color: 0, 1, 1, 1  # Неоновый циан
        bold: True
        size_hint_y: 0.25
    
    # Кнопка клика
    Button:
        text: '💖 КЛИКНИ!'
        font_size: '28sp'
        background_color: 1, 0.5, 1, 0.9  # Розовый
        color: 0, 0, 0, 1  # Чёрный текст
        size_hint_y: 0.3
        on_release: app.add_point()
    
    # Кнопка сброса
    Button:
        text: '🔄 Сброс'
        font_size: '18sp'
        background_color: 0.3, 0.3, 0.4, 0.8
        size_hint_y: 0.15
        on_release: app.reset_score()
"""

Builder.load_string(KV_CODE)

from kivy.uix.boxlayout import BoxLayout

class MainLayout(BoxLayout):
    pass

class Y2KClickerApp(App):
    score = NumericProperty(0)
    
    def build(self):
        return MainLayout()  # Обязательно возвращаем корневой виджет!
    
    def add_point(self):
        self.score += 1
    
    def reset_score(self):
        self.score = 0

if __name__ == '__main__':
    Y2KClickerApp().run()