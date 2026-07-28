# main.py
import random
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

Window.clearcolor = (0.02, 0.02, 0.08, 1)

# ================= KV STYLE & LAYOUTS =================
KV = '''
#:import utils kivy.utils

<CyberLabel@Label>:
    font_size: '26sp'
    color: 0, 1, 1, 1
    halign: 'center'
    valign: 'middle'

<CyberButton@Button>:
    background_color: 0, 0, 0, 0
    color: 1, 0.9, 0.2, 1
    font_size: '20sp'
    size_hint_y: 0.15
    canvas.before:
        Color:
            rgba: 0.05, 0.05, 0.15, 1
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: 0, 1, 1, 1 if self.state == 'normal' else 1, 0, 0.8, 1
        Line:
            rectangle: self.x+2, self.y+2, self.width-4, self.height-4
            width: 2.5

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 20
        canvas.before:
            Color:
                rgba: 0.02, 0.02, 0.08, 1
            Rectangle:
                pos: self.pos
                size: self.size
        CyberLabel:
            id: title
            text: '🎮 CYBER GAMES 🎮'
            font_size: '38sp'
            color: 1, 0.8, 0, 1
            size_hint_y: 0.2
        GridLayout:
            cols: 1
            spacing: 15
            size_hint_y: 0.6
            CyberButton:
                text: '✊✋✌️ Камень Ножницы Бумага'
                on_press: root.manager.current = 'rps'
            CyberButton:
                text: '🐍 Змейка'
                on_press: root.manager.current = 'snake'
            CyberButton:
                text: '❌⭕ Крестики Нолики'
                on_press: root.manager.current = 'tictactoe'
        Label:
            text: 'v1.0 | Kivy + Python | Cyberpunk Edition'
            font_size: '14sp'
            color: 0.4, 0.4, 0.6, 1
            size_hint_y: 0.1

<GameScreen@Screen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 15
        CyberLabel:
            id: title
            text: root.title
            font_size: '30sp'
            color: 1, 0.8, 0, 1
            size_hint_y: 0.12
        BoxLayout:
            id: game_area
            size_hint_y: 0.7
        CyberButton:
            text: '◀ НАЗАД В МЕНЮ'
            on_press: root.manager.current = 'menu'
'''

Builder.load_string(KV)

# ================= SCREENS =================
class MenuScreen(Screen):
    def on_enter(self, *args):
        # Пульсация заголовка при входе
        Animation(color=(0, 1, 1, 1), duration=0.5) + Animation(color=(1, 0.8, 0, 1), duration=0.5)).start(self.ids.title)

class RPSScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'КАМЕНЬ НОЖНИЦЫ БУМАГА'
        layout = BoxLayout(orientation='vertical', padding=10, spacing=15)
        self.result = CyberLabel(text='Выбери оружие!', size_hint_y=0.25)
        grid = GridLayout(cols=3, spacing=10, size_hint_y=0.6)
        for txt, choice in [('🪨 Камень','rock'), ('📄 Бумага','paper'), ('✂️ Ножницы','scissors')]:
            btn = CyberButton(text=txt, font_size='22sp')
            btn.bind(on_press=lambda x, c=choice: self.play(c))
            grid.add_widget(btn)
        reset = CyberButton(text='🔄 Сброс', size_hint_y=0.15)
        reset.bind(on_press=lambda x: self.reset())
        layout.add_widget(self.result)
        layout.add_widget(grid)
        layout.add_widget(reset)
        self.add_widget(layout)

    def play(self, player):
        comp = random.choice(['rock', 'paper', 'scissors'])
        wins = {'rock':'scissors', 'paper':'rock', 'scissors':'paper'}
        if player == comp: res = '🤝 Ничья!'
        elif wins[player] == comp: res = f'🎉 Победа! {player} > {comp}'
        else: res = f'💀 Проигрыш! {comp} > {player}'
        self.result.text = res
        Animation(opacity=0, d=0.1) + Animation(opacity=1, d=0.3)).start(self.result)

    def reset(self, *args): self.result.text = 'Выбери оружие!'

class TicTacToeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'КРЕСТИКИ НОЛИКИ'
        self.board = [''] * 9
        self.turn = 'X'
        self.over = False
        layout = BoxLayout(orientation='vertical', padding=10, spacing=15)
        self.status = CyberLabel(text='Ход: X', size_hint_y=0.2)
        grid = GridLayout(cols=3, spacing=5, size_hint_y=0.7)
        self.btns = []
        for i in range(9):
            b = Button(text='', font_size='36sp', color=(0.8,0.8,0.8,1), background_color=(0.05,0.05,0.1,1))
            b.bind(on_press=lambda x, i=i: self.move(i))
            grid.add_widget(b)
            self.btns.append(b)
        reset = CyberButton(text='🔄 Новая игра', size_hint_y=0.1)
        reset.bind(on_press=lambda x: self.reset())
        layout.add_widget(self.status)
        layout.add_widget(grid)
        layout.add_widget(reset)
        self.add_widget(layout)

    def move(self, i):
        if self.board[i] == '' and not self.over:
            self.board[i] = self.turn
            self.btns[i].text = self.turn
            self.btns[i].color = (1, 0.2, 0.8, 1) if self.turn == 'X' else (0, 1, 1, 1)
            if self.check_win():
                self.status.text = f'🏆 {self.turn} победил!'
                self.over = True
            elif '' not in self.board:
                self.status.text = '🤝 Ничья!'
                self.over = True
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                self.status.text = f'Ход: {self.turn}'

    def check_win(self):
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        return any(self.board[a]==self.board[b]==self.board[c] and self.board[a]!='' for a,b,c in lines)

    def reset(self, *args):
        self.board, self.turn, self.over = ['']*9, 'X', False
        for b in self.btns: b.text = ''
        self.status.text = 'Ход: X'

class SnakeWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = 20
        self.cell = 20
        self.size = (self.grid * self.cell, self.grid * self.cell)
        self.snake = [(10, 10)]
        self.dir = (1, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.over = False
        Clock.schedule_interval(self.update, 0.15)

    def spawn_food(self):
        while True:
            p = (random.randint(0, self.grid-1), random.randint(0, self.grid-1))
            if p not in self.snake: return p

    def update(self, dt):
        if self.over: return
        hx, hy = self.snake[0]
        nh = (hx + self.dir[0], hy + self.dir[1])
        if nh[0]<0 or nh[0]>=self.grid or nh[1]<0 or nh[1]>=self.grid or nh in self.snake:
            self.over = True
            self.parent.parent.ids.game_status.text = f'💀 Game Over! Счёт: {self.score}'
            return
        self.snake.insert(0, nh)
        if nh == self.food:
            self.score += 1
            self.food = self.spawn_food()
        else: self.snake.pop()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.02, 0.02, 0.08)
            Rectangle(pos=self.pos, size=self.size)
            # Змейка
            Color(0, 1, 0.8)
            for sx, sy in self.snake:
                Rectangle(pos=(self.x + sx*self.cell, self.y + sy*self.cell), size=(self.cell-2, self.cell-2))
            # Еда
            Color(1, 0.2, 0.5)
            Rectangle(pos=(self.x + self.food[0]*self.cell, self.y + self.food[1]*self.cell), size=(self.cell-2, self.cell-2))

    def change_dir(self, d):
        dirs = {'up':(0,1), 'down':(0,-1), 'left':(-1,0), 'right':(1,0)}
        nd = dirs[d]
        if nd[0]+self.dir[0]!=0 or nd[1]+self.dir[1]!=0: self.dir = nd

    def reset(self):
        self.snake, self.dir, self.food, self.score, self.over = [(10,10)], (1,0), self.spawn_food(), 0, False
        self.canvas.clear()

class SnakeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'ЗМЕЙКА'
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.game_status = CyberLabel(text='Счёт: 0', size_hint_y=0.1)
        self.snake_w = SnakeWidget(size_hint_y=0.6)
        self.snake_w.bind(pos=lambda w, v: self.center_widget(w))
        controls = GridLayout(cols=4, spacing=5, size_hint_y=0.2)
        for d, txt in [('up','⬆️'), ('left','⬅️'), ('down','⬇️'), ('right','➡️')]:
            b = CyberButton(text=txt, font_size='20sp')
            b.bind(on_press=lambda x, d=d: self.snake_w.change_dir(d))
            controls.add_widget(b)
        reset = CyberButton(text='🔄 Рестарт', size_hint_y=0.1)
        reset.bind(on_press=lambda x: self.snake_w.reset())
        layout.add_widget(self.game_status)
        layout.add_widget(self.snake_w)
        layout.add_widget(controls)
        layout.add_widget(reset)
        self.add_widget(layout)

    def center_widget(self, w):
        # Центрирование игрового поля внутри layout
        if self.ids.game_area:
            w.pos = (self.ids.game_area.x, self.ids.game_area.y + (self.ids.game_area.height - w.height)/2)

    def on_enter(self, *args): self.snake_w.reset()

# ================= APP =================
class CyberGamesApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(RPSScreen(name='rps'))
        sm.add_widget(TicTacToeScreen(name='tictactoe'))
        sm.add_widget(SnakeScreen(name='snake'))
        return sm

if __name__ == '__main__':
    CyberGamesApp().run()