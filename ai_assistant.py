import os
import customtkinter as ctk
import google.generativeai as genai

# --- 1. استدعاء المفتاح المحفوظ من خبايا الجهاز تلقائياً ---
api_key_from_system = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key_from_system)

# اختيار النموذج السحابي السريع والذكي
model = genai.GenerativeModel('gemini-2.5-flash')

# --- 2. إعدادات مظهر الواجهة الرسومية ---
ctk.set_appearance_mode("dark")       # الوضع المظلم المريح للعين
ctk.set_default_color_theme("green")    # اللون الأزرق الذكي للأزرار

class OnlineChatBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # إعدادات أبعاد النافذة وعنوانها
        self.title("Tiny assistant (Online)")
        self.geometry("450x600")
        
        # --- تصميم عناصر الواجهة (GUI Widgets) ---
        
        # أولاً: عنوان البرنامج في الأعلى
        self.title_label = ctk.CTkLabel(
            self, 
            text="Tiny assistant is in your service!", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        # ثانياً: صندوق عرض المحادثة (Scrollable Text Box)
        self.chat_box = ctk.CTkTextbox(
            self, 
            width=410, 
            height=430, 
            font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.chat_box.pack(padx=20, pady=5)
        self.chat_box.configure(state="disabled") # جعله للقراءة فقط حتى لا يمسح المستخدم النصوص بالخطأ
        
        # طباعة رسالة ترحيبية عند فتح البرنامج
        self.display_message("AI: Hi programmer! I'm your tiny assistant. Ask me what do you want about programming, and I'll do my best to help you out!")
        
        # ثالثاً: إطار سفلي يجمع صندوق الكتابة وزر الإرسال في سطر واحد
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(padx=20, pady=15, fill="x")
        
        # صندوق إدخال النص (حيث تكتب سؤالك)
        self.entry_box = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="Write your question here...", 
            width=310, 
            font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_box.pack(side="left", padx=(0, 10))
        
        # ربط زر التعديل (Enter) ليرسل الرسالة فوراً عند الضغط عليه من لوحة المفاتيح
        self.entry_box.bind("<Return>", lambda event: self.send_message())
        
        # زر الإرسال الأزرق
        self.send_button = ctk.CTkButton(
            self.input_frame, 
            text="Submit", 
            width=80, 
            command=self.send_message
        )
        self.send_button.pack(side="right")

    def display_message(self, text):
        """دالة مخصصة لطباعة النصوص داخل صندوق المحادثة وتمرير الشاشة للأسفل تلقائياً"""
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", text + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.yview("end") # النزول التلقائي لآخر رسالة

    def send_message(self):
        """الدالة الأساسية لمعالجة الإرسال والاتصال بجوجل"""
        user_text = self.entry_box.get()
        if not user_text.strip(): # إذا كان الصندوق فارغاً، لا تفعل شيئاً
            return
            
        # 1. عرض سؤالك أنت أولاً في الشات
        self.display_message(f"You: {user_text}")
        self.entry_box.delete(0, "end") # تنظيف صندوق الكتابة ليصبح جاهزاً للسؤال التالي
        
        try:
            # 2. إرسال السؤال إلى سيرفرات جوجل واستقبال الإجابة
            response = model.generate_content(user_text)
            ai_response = response.text
            
            # 3. عرض إجابة الذكاء الاصطناعي في الشات
            self.display_message(f"AI: {ai_response}")
            self.display_message("-" * 40) # خط فاصل للتنظيم
            
        except Exception as e:
            # في حال حدوث أي خطأ (مثل انقطاع مفاجئ للإنترنت أو عدم العثور على المفتاح)
            self.display_message("Error: Something went wrong while connecting to the AI service. Please check your internet connection and API key.")

# --- 3. تشغيل التطبيق الرسومي ---
if __name__ == "__main__":
    app = OnlineChatBotApp()
    app.mainloop()
