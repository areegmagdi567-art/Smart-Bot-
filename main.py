import os
import google.generativeai as genai
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# إعداد مفتاح API الخاص بجيميناي
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # استبدل هذا بمفتاحك
genai.configure(api_key=GEMINI_API_KEY)

# معلومات لوائح الكلية لتغذية الذكاء الاصطناعي
COLLEGE_RULES = """
أنت مساعد ذكي ومتخصص في الإجابة عن لوائح الكلية للطلاب.
لوائح الكلية:
- نسبة الحضور المطلوبة لدخول الامتحان: 75%.
- الحد الأقصى للمواد المتبقية للترفيع: مادتين فقط.
- نظام التقديرات: الممتاز (85%+)، الجيد جداً (75%-84%)، الجيد (65%-74%)، المقبول (50%-64%).
- يجب تقديم الأعذار الطبية خلال 48 ساعة من تاريخ الامتحان.
إصدار الإجابات بأسلوب ودود، واضح، ومباشر.
"""

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=COLLEGE_RULES
)

class ChatMessage(MDCard):
    """مكون يمثل فقاعة الرسالة مع زوايا دائرية وألوان كحلية"""
    def __init__(self, text, is_user=True, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.radius = [18, 18, 4, 18] if is_user else [18, 18, 18, 4]
        self.padding = "12dp"
        self.margin_hint = [0.05, 0.05]
        
        # درجات الكحلي: فاتح للترويسة/المستخدم، وغامق للبوت
        self.md_bg_color = [0.12, 0.23, 0.37, 1] if is_user else [0.05, 0.10, 0.20, 1]
        
        label = MDLabel(
            text=text,
            halign="right",
            theme_text_color="Custom",
            text_color=[0.9, 0.95, 1, 1],
            size_hint_y=None,
            font_style="Body1"
        )
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        self.add_widget(label)
        self.bind(children=lambda instance, value: setattr(self, 'height', label.height + 24))

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # الخلفية الرئيسية - كحلي ملكي عميق
        self.md_bg_color = [0.03, 0.06, 0.13, 1]
        
        main_layout = MDBoxLayout(orientation='vertical')
        
        # شريط العنوان العلوي (Header)
        header = MDCard(
            size_hint_y=0.1,
            md_bg_color=[0.08, 0.16, 0.28, 1],
            radius=[0, 0, 20, 20],
            padding="15dp"
        )
        header_title = MDLabel(
            text="🎓 مرشد الكلية الذكي",
            halign="center",
            bold=True,
            font_style="H6",
            theme_text_color="Custom",
            text_color=[0.4, 0.7, 1, 1]
        )
        header.add_widget(header_title)
        main_layout.add_widget(header)
        
        # منطقة المحادثة والإشعارات
        self.scroll = ScrollView(size_hint=(1, 0.78))
        self.chat_list = MDBoxLayout(
            orientation='vertical',
            spacing="10dp",
            padding="10dp",
            size_hint_y=None
        )
        self.chat_list.bind(minimum_height=self.chat_list.setter('height'))
        self.scroll.add_widget(self.chat_list)
        main_layout.add_widget(self.scroll)
        
        # شريط الإدخال السفلي
        input_box = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=0.12,
            padding="10dp",
            spacing="10dp"
        )
        
        self.text_input = MDTextField(
            hint_text="اسأل عن اللوائح والامتحانات...",
            mode="round",
            fill_color_normal=[0.08, 0.16, 0.28, 1],
            text_color_normal=[1, 1, 1, 1],
            hint_text_color_normal=[0.6, 0.7, 0.8, 1],
            size_hint_x=0.85
        )
        
        send_btn = MDFloatingActionButton(
            icon="send",
            md_bg_color=[0.2, 0.45, 0.75, 1],
            icon_color=[1, 1, 1, 1],
            on_release=self.send_message
        )
        
        input_box.add_widget(self.text_input)
        input_box.add_widget(send_btn)
        main_layout.add_widget(input_box)
        
        self.add_widget(main_layout)

    def send_message(self, instance):
        user_text = self.text_input.text.strip()
        if not user_text:
            return
            
        self.chat_list.add_widget(ChatMessage(text=user_text, is_user=True))
        self.text_input.text = "عذراً، حدث خطأ أثناء الاتصال بالخادم "
        
        try:
            response = model.generate_content(user_text)
            bot_reply = response.text
        except Exception as e:
            bot_reply = ""
        self.chat_list.add_widget(ChatMessage(text=bot_reply, is_user=False))

class CollegeBotApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        return MainScreen()

if __name__ == "__main__":
    CollegeBotApp().run()
