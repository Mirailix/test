# screens.py
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock
from kivy.app import App
import random


class MainMenuScreen(Screen):
    """Главное меню"""
    
    def start_game1(self):
        """Переход к игре 1"""
        self.manager.current = 'game1'
        self.manager.get_screen('game1').reset_game()
    
    def start_game2(self):
        """Переход к игре 2"""
        self.manager.current = 'game2'
        self.manager.get_screen('game2').reset_game()
    
    def open_settings(self):
        """Открыть настройки"""
        self.manager.current = 'settings'


class Game1Screen(Screen):
    """Игра 1: 'Кликни неон' — кликай по появляющимся объектам"""
    
    score = NumericProperty(0)
    time_left = NumericProperty(30)
    game_active = False
    
    def reset_game(self):
        """Сброс игры"""
        self.score = 0
        self.time_left = 30
        self.game_active = True
        # Запускаем таймер (реализуется в .kv через Clock)
    
    def add_score(self, points):
        """Добавить очки"""
        if self.game_active:
            self.score += points
            # Обновляем глобальный счёт в главном приложении
            app = App.get_running_app()
            app.current_score = self.score
    
    def end_game(self):
        """Завершение игры"""
        self.game_active = False
        # Показать результат, вернуться в меню


class Game2Screen(Screen):
    """Игра 2: 'Y2K Пазл' — собери изображение"""
    
    puzzle_solved = False
    moves_count = NumericProperty(0)
    
    def reset_game(self):
        """Сброс пазла"""
        self.puzzle_solved = False
        self.moves_count = 0
        # Здесь логика перемешивания частей пазла
    
    def check_win(self):
        """Проверка победы"""
        if all_parts_in_place():  # ваша функция проверки
            self.puzzle_solved = True
            app = App.get_running_app()
            app.current_score += 100


class SettingsScreen(Screen):
    """Экран настроек"""
    
    def save_name(self, name):
        """Сохранить имя игрока"""
        app = App.get_running_app()
        app.player_name = name
    
    def change_theme(self, color):
        """Сменить цветовую тему"""
        app = App.get_running_app()
        app.theme_color = color
    
    def go_back(self):
        """Вернуться в меню"""
        self.manager.current = 'main_menu'