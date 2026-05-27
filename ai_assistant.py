import os
from tkinter import filedialog
import customtkinter as ctk
import google.generativeai as genai
import traceback  # مكتبة مخصصة لطباعة تفاصيل الأخطاء كاملة في الـ Terminal

# --- 1. إعداد المفتاح ---
# ⚠️ ضع مفتاحك الجديد النشط هنا ليعمل البرنامج فوراً وبدون أخطاء
api_key_from_system = "YOUR_REAL_API_KEY"
genai.configure(api_key=api_key_from_system)

# اختيار النموذج السحابي السريع والذكي مع التعليمات الشاملة
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=(
        "Your name is 'Tiny assistant'. You are a helpful AI programming assistant. "
        "You must answer in the same language the user speaks. " 
        "You can answer questions about programming, provide code snippets, and explain programming concepts. "
        "If you don't know the answer, say 'I don't know' instead of making up an answer." 
        "Always be concise and to the point. Avoid unnecessary explanations. "
        "Focus on providing clear and direct answers to the user's programming questions."
    )
)

# --- 2. إعدادات مظهر الواجهة الرسومية ---
ctk.set_appearance_mode("dark")       
ctk.set_default_color_theme("green")    

class OnlineChatBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # ذاكرة نصية مبسطة تجمع الحوار على شكل نص مستمر لحماية الاتصال من التداخل
        self.chat_history_text = ""
        
        self.title("Tiny assistant (Online)")
        self.geometry("450x600")
        
        # --- عناصر الواجهة ---
        self.title_label = ctk.CTkLabel(
            self, text="Tiny assistant is in your service!", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        self.chat_box = ctk.CTkTextbox(
            self, width=410, height=430, font=ctk.CTkFont(family="Segoe UI", size=14)
        )
        self.chat_box.pack(padx=20, pady=5)
        self.chat_box.configure(state="disabled") 
        
        self.display_message("AI: Hi programmer! I'm your tiny assistant. Ask me what do you want about programming, and I'll do my best to help you out!")
        
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(padx=20, pady=15, fill="x")
        
        self.entry_box = ctk.CTkEntry(
            self.input_frame, placeholder_text="Write your question here...", 
            width=210, font=ctk.CTkFont(family="Segoe UI", size=13)
        )
        self.entry_box.pack(side="left", padx=(0, 5))
        self.entry_box.bind("<Return>", lambda event: self.send_message())
        
        self.send_button = ctk.CTkButton(self.input_frame, text="Submit", width=70, command=self.send_message)
        self.send_button.pack(side="right")

        self.upload_button = ctk.CTkButton(
            self.input_frame, text="Upload File", width=90, 
            fg_color="#1f538d", hover_color="#14375e", command=self.upload_and_fix_file
        )
        self.upload_button.pack(side="right", padx=(0, 5))

    def display_message(self, text):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", text + "\n")
        self.chat_box.configure(state="disabled")
        self.chat_box.yview("end") 

    def send_message(self):
        user_text = self.entry_box.get()
        if not user_text.strip(): 
            return
            
        self.display_message(f"You: {user_text}")
        self.entry_box.delete(0, "end") 
        
        try:
            # بناء الطلب بدمج التاريخ السابق مع السؤال الحالي
            self.chat_history_text += f"\nUser: {user_text}\n"
            
            # إرسال الطلب
            response = model.generate_content(self.chat_history_text)
            ai_response = response.text
            
            # حفظ إجابة الـ AI في التاريخ
            self.chat_history_text += f"AI: {ai_response}\n"
            
            self.display_message(f"AI: {ai_response}")
            self.display_message("-" * 40) 
            
        except Exception as e:
            # طباعة تفاصيل الخطأ في الـ Terminal لمعرفته فوراً
            print("\n" + "="*50 + " DETECTED ERROR " + "="*50)
            traceback.print_exc()
            print("="*116 + "\n")
            
            self.display_message("Error: Something went wrong. Check VS Code Terminal for the real error!")

    def upload_and_fix_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py"), ("All Files", "*.*")])
        if not file_path: return
            
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code_content = file.read()
            
            file_name = os.path.basename(file_path)
            self.display_message(f"You: [Uploaded File: {file_name}]")
            
            prompt = f"Review this code from '{file_name}', check for any errors, fix them, and provide the corrected code with a brief explanation:\n\n{code_content}"
            self.chat_history_text += f"\nUser: {prompt}\n"
            
            response = model.generate_content(self.chat_history_text)
            ai_response = response.text
            
            self.chat_history_text += f"AI: {ai_response}\n"
            self.display_message(f"AI:\n{ai_response}")
            self.display_message("-" * 40)
            
        except Exception as e:
            print("\n" + "="*50 + " UPLOAD ERROR " + "="*50)
            traceback.print_exc()
            print("="*114 + "\n")
            self.display_message("Error: Could not read file. Check Terminal.")

if __name__ == "__main__":
    app = OnlineChatBotApp()
    app.mainloop()
