import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.config import Config

# 设置图形兼容性配置
Config.set('graphics', 'multisamples', '0')  # 禁用多重采样以提高兼容性
Config.set('kivy', 'log_level', 'warning')   # 减少日志输出

# 定义扑克牌
suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '小王', '大王']
deck = [(rank, suit) for suit in suits for rank in ranks[:-2]]  # 普通牌
deck.extend([(ranks[-2], ''), (ranks[-1], '')])  # 添加大小王

# 定义牌对应的值
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 11, 'Q': 12, 'K': 13, 'A': 14, '小王': 0, '大王': 0
}

# 检查是否能计算出24
def calculate_24(numbers):
    from itertools import permutations
    from operator import add, sub, mul, truediv

    operators = [add, sub, mul, truediv]
    for nums in permutations(numbers):
        for op1 in operators:
            for op2 in operators:
                for op3 in operators:
                    try:
                        # 计算顺序：((a op1 b) op2 c) op3 d
                        result = op3(op2(op1(nums[0], nums[1]), nums[2]), nums[3])
                        if abs(result - 24) < 1e-6:  # 允许浮点数误差
                            return True
                    except ZeroDivisionError:
                        continue
    return False

# 游戏主界面
class GameApp(App):
    def build(self):
        self.title = "24点游戏"
        # 如果图标文件不存在，跳过设置图标
        try:
            self.icon = "rabbit.png"  # 设置应用图标
        except:
            pass
            
        # 设置窗口大小和兼容性
        Window.clearcolor = (1, 1, 1, 1)  # 设置白色背景
        Window.size = (400, 600)  # 设置窗口大小

        # 主布局
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # 兔子头图片 - 添加错误处理
        try:
            self.rabbit_image = Image(source='rabbit.png', size_hint=(1, 0.4))
            self.layout.add_widget(self.rabbit_image)
        except:
            # 如果图片加载失败，用标签代替
            self.rabbit_image = Label(text="24点游戏", font_size=30, size_hint=(1, 0.4))
            self.layout.add_widget(self.rabbit_image)

        # 显示牌和值
        self.card_label = Label(
            text="等待抽牌...", 
            font_size=20, 
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1)  # 黑色文字
        )
        self.layout.add_widget(self.card_label)

        # 用户输入框
        self.input_box = TextInput(
            hint_text="输入表达式（例如 (11 + 13) * (12 - 10)）", 
            size_hint=(1, 0.2),
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )
        self.layout.add_widget(self.input_box)

        # 提交按钮
        self.submit_button = Button(
            text="提交", 
            size_hint=(1, 0.2),
            background_color=(0.2, 0.6, 1, 1)  # 蓝色按钮
        )
        self.submit_button.bind(on_press=self.check_answer)
        self.layout.add_widget(self.submit_button)

        # 初始化游戏
        self.remaining_deck = deck.copy()
        self.score = 0
        self.draw_cards()

        return self.layout

    # 抽牌逻辑
    def draw_cards(self):
        if len(self.remaining_deck) >= 4:
            self.selected_cards = random.sample(self.remaining_deck, 4)
            self.selected_values = [card_values[card[0]] for card in self.selected_cards]

            # 检查是否能计算出24
            if not calculate_24(self.selected_values):
                self.draw_cards()  # 重新抽牌
                return

            # 更新界面显示
            self.card_label.text = f"抽取的牌: {self.selected_cards}\n对应的值: {self.selected_values}"
        else:
            self.card_label.text = "游戏结束！牌堆中剩余的牌不足4张。"
            self.submit_button.disabled = True

    # 检查用户答案
    def check_answer(self, instance):
        user_input = self.input_box.text
        try:
            # 检查用户输入的表达式是否使用了正确的牌
            used_numbers = []
            for value in self.selected_values:
                if str(value) not in user_input:
                    self.show_popup("错误", f"未使用牌值 {value}")
                    return
                used_numbers.append(value)

            # 计算用户表达式的结果
            result = eval(user_input)
            if abs(result - 24) < 1e-6:
                self.show_popup("恭喜", "计算正确！")
                self.score += 1
                # 移除已使用的牌
                for card in self.selected_cards:
                    if card in self.remaining_deck:
                        self.remaining_deck.remove(card)
                self.draw_cards()
            else:
                self.show_popup("错误", f"计算结果为 {result}，不是24。")
        except Exception as e:
            self.show_popup("错误", f"输入无效: {e}")

    # 显示弹窗
    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, font_size=20, color=(0, 0, 0, 1))
        popup_button = Button(text="关闭", size_hint=(1, 0.2))
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(
            title=title, 
            content=popup_layout, 
            size_hint=(0.8, 0.4),
            background='atlas://data/images/defaulttheme/button'
        )
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

# 启动游戏
if __name__ == "__main__":
    GameApp().run()