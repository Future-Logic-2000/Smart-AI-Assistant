import os
import re
from tkinter import filedialog
import customtkinter as ctk
import google.generativeai as genai
import traceback

# --- 1. إعداد المفتاح ---
api_key_from_system = "YOUR_REAL_API_KEY"
genai.configure(api_key=api_key_from_system)

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=(
        "Your name is 'Tiny assistant'. You are a helpful AI programming assistant. "
        "You must answer in the same language the user speaks. " 
        "You can answer questions about programming, provide code snippets, and explain programming concepts. "
        "If you don't know the answer, say 'I don't know' instead of making up an answer." 
        "Always be concise and to the point. Focus on providing clear, numbered, or bulleted direct answers to the user's programming questions. "
        "Format your code and explanations cleanly so they are easy to read."
    )
)

# --- 2. إعدادات مظهر الواجهة الرسومية ---
ctk.set_appearance_mode("dark")       
ctk.set_default_color_theme("green")    

class OnlineChatBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.chat_history_text = ""
        
        self.title("Tiny assistant (Online)")
        self.geometry("520x700")  # تم تكبير الأبعاد قليلاً لتوفير مساحة مريحة للتنسيق الجديد
        
        # --- عناصر الواجهة ---
        self.title_label = ctk.CTkLabel(
            self, text="Tiny assistant is in your service!", 
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold")
        )
        self.title_label.pack(pady=15)
        
        self.chat_box = ctk.CTkTextbox(
            self, width=480, height=500, font=ctk.CTkFont(family="Segoe UI", size=14), wrap="word"
        )
        self.chat_box.pack(padx=20, pady=5)
        
        # إعداد الخطوط والتنسيقات داخل صندوق النص
        self.chat_box._textbox.tag_configure("rtl", justify="right")
        self.chat_box._textbox.tag_configure("ltr", justify="left")
        self.chat_box._textbox.tag_configure("bold_font", font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"))
        self.chat_box._textbox.tag_configure("code_font", font=ctk.CTkFont(family="Consolas", size=13), foreground="#ff79c6")
        
        self.chat_box.configure(state="disabled") 
        
        self.display_message("AI: Hi programmer! I'm your tiny assistant. Ask me what do you want about programming, and I'll do my best to help you out!")
        self.display_message("—" * 40)
        
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(padx=20, pady=15, fill="x")
        
        self.entry_box = ctk.CTkEntry(
            self.input_frame, placeholder_text="Write your question here...", 
            width=260, font=ctk.CTkFont(family="Segoe UI", size=13)
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
        
        # تحديد اتجاه النص بناءً على وجود حروف عربية
        is_arabic = bool(re.search(r"[\u0600-\u06FF]", text))
        base_tag = "rtl" if is_arabic else "ltr"
        
        # تقسيم النص إلى أسطر لمعالجتها وتنسيقها بشكل جميل
        lines = text.split('\n')
        for line in lines:
            if not line.strip():
                self.chat_box.insert("end", "\n", base_tag)
                continue
                
            # 1. تنظيف علامات النقاط المشوهة واستبدالها بنقاط تنظيمية أنيقة (•)
            clean_line = re.sub(r"^\s*[\*\-]\s+", "  •  ", line)
            
            # 2. رصد النصوص العريضة بين النجوم مثل **النص** وتطبيق خط عريض مخصص لها
            parts = re.split(r"(\*\*.*?\*\*)", clean_line)
            
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    # إزالة النجوم وعرض الكلمة بخط عريض وملون
                    bold_text = part[2:-2]
                    self.chat_box.insert("end", bold_text, (base_tag, "bold_font"))
                elif part.startswith("`") and part.endswith("`"):
                    # إذا كان كوداً برمجياً صغيراً
                    code_text = part[1:-1]
                    self.chat_box.insert("end", f" {code_text} ", (base_tag, "code_font"))
                else:
                    self.chat_box.insert("end", part, base_tag)
                    
            self.chat_box.insert("end", "\n", base_tag)
            
        self.chat_box.configure(state="disabled")
        self.chat_box.yview("end") 

    def send_message(self):
        user_text = self.entry_box.get()
        if not user_text.strip(): 
            return
            
        self.display_message(f"You: {user_text}")
        self.entry_box.delete(0, "end") 
        
        try:
            self.chat_history_text += f"\nUser: {user_text}\n"
            response = model.generate_content(self.chat_history_text)
            ai_response = response.text
            
            self.chat_history_text += f"AI: {ai_response}\n"
            self.display_message(f"AI: {ai_response}")
            self.display_message("—" * 40)  
            
        except Exception as e:
            print("\n" + "="*50 + " DETECTED ERROR " + "="*50)
            traceback.print_exc()
            print("="*116 + "\n")
            self.display_message("Error: Something went wrong. Check VS Code Terminal.")

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
            self.display_message("—" * 40)  
            
        except Exception as e:
            print("\n" + "="*50 + " UPLOAD ERROR " + "="*50)
            traceback.print_exc()
            print("="*114 + "\n")
            self.display_message("Error: Could not read file.")

if __name__ == "__main__":
    app = OnlineChatBotApp()
    app.mainloop()
